import pickle
import rsa
import socket
import ntplib
from contextlib import closing

ntp_client = ntplib.NTPClient()

TIMEOUT = 100
PKDA_PORT = 2222
B_PORT = 4444
MSG_SIZE = 512

class Packet:
    def __init__(self, sender, request, time, reply = None, nonce = 0):
        self.sender = sender
        self.request = request
        self.time = time
        self.reply = reply
        self.nonce = nonce
    def encode(self):
        return pickle.dumps(self)

class Client:

    def __init__(self,client="B"):
        self.client = client
        self.keys = {}
        self.port = B_PORT

        with open('Client'+self.client+'.pkl', 'rb') as f:
            d = pickle.load(f)
            self.keys["public"] = d["public"]
            self.keys["private"] = d["private"]
        with open('PKDA.pkl', 'rb') as f:
            d = pickle.load(f)
            self.keys["PKDA"] = d["private"]
            

    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        self.s.bind((HOST,self.port))
        print("Client "+self.client+"  listening to port "+str(self.port))
        self.s.listen()

    def get_trgt_socket(self,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host ="127.0.0.1"
        s.connect((host,port))
        return s

    def create_request(self,msg,nonce=0):
        response = ntp_client.request('uk.pool.ntp.org', version=3)
        cur_time = response.tx_time
        packet = Packet(self.client,msg,cur_time,nonce=nonce)
        return packet

    def getKey(self):

        # Query from A
        (clientsocket, address) = self.s.accept()
        msg = clientsocket.recv(MSG_SIZE)
        # msg = rsa.decrypt(msg, self.keys["private"])
        A_data = pickle.loads(msg)
        A_nonce = A_data.nonce

        print("Received Request from A")

        # Communicate with pkda
        pkda_req = self.create_request("A")
        msg = pkda_req.encode()
        self.pkda_sock = self.get_trgt_socket(PKDA_PORT)
        self.pkda_sock.send(msg)

        print("Sent Public Key Request to PKDA")

        msg = self.pkda_sock.recv(MSG_SIZE)
        # msg = rsa.decrypt(msg, self.keys["PKDA"])
        data = pickle.loads(msg)
        self.keys["A"] = data.reply
        self.pkda_sock.close()

        print("Received public key of A from PKDA")

        # Reply to A
        A_rep = self.create_request(A_nonce,nonce=A_nonce+1)
        msg = A_rep.encode()
        # msg = rsa.encrypt(msg,self.keys["A"])
        clientsocket.send(msg)

        print("Sent Ack to A")

        # Confirmation from A
        msg = clientsocket.recv(MSG_SIZE)
        # msg = rsa.decrypt(msg, self.keys["private"])
        A_data = pickle.loads(msg)

        if A_data.nonce != (A_nonce+1):
            print("Oops")
            self.s.close()
            return 0

        print("Received Ack from A")
        
        self.clientsocket = clientsocket

        return 1

    def communicate(self):

        for i in range(1,4):

            msg = self.clientsocket.recv(MSG_SIZE)
            # msg = rsa.decrypt(msg, self.keys["private"])
            A_data = pickle.loads(msg)
            print("Message Received from ",A_data.sender," saying - ",A_data.request)

            A_rep = self.create_request("Got it - "+str(A_data.nonce),A_data.nonce+1)
            msg = A_rep.encode()
            # msg = rsa.encrypt(msg,self.keys["A"])
            self.clientsocket.send(msg)

        self.clientsocket.close()
        self.s.close()






clientB = Client("B")
clientB.create_socket()
if clientB.getKey():
    clientB.communicate()




