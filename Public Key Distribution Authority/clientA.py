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

    def __init__(self,client="A"):
        self.client = client
        self.keys = {}
        self.port = 3333

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
        print("Client "+self.client+"  connected to port "+str(self.port))
        self.s.listen()

    def get_trgt_socket(self,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host ="127.0.0.1"
        s.connect((host,port))
        return s

    def create_request(self,msg,nonce=0):
        response = ntp_client.request('uk.pool.ntp.org', version=3)
        cur_time = response.tx_time
        packet = Packet("A",msg,cur_time,nonce=nonce)
        return packet

    def getKey(self):

        # Communicate with pkda
        pkda_req = self.create_request("B")
        msg = pkda_req.encode()
        self.pkda_sock = self.get_trgt_socket(PKDA_PORT)
        self.pkda_sock.send(msg)

        print("Sent Request to PKDA for Public Key of B")

        msg = self.pkda_sock.recv(MSG_SIZE)
        msg = rsa.decrypt(msg, self.keys["PKDA"])
        data = pickle.loads(msg)
        self.keys["B"] = data.reply
        self.pkda_sock.close()
        print("Received Public Key of B from PKDA ")

        # Communicate with B
        nonce = 100
        B_req = self.create_request(str(self.port),nonce=nonce)
        msg = B_req.encode()
        # msg = rsa.encrypt(msg,self.keys["B"])
        self.B_sock = self.get_trgt_socket(B_PORT)
        self.B_sock.send(msg)

        print("Sent Communication Request to B")

        msg = self.B_sock.recv(MSG_SIZE)
        # msg = rsa.decrypt(msg, self.keys["private"])
        data = pickle.loads(msg)

        print("Received Response from B")

        if data.nonce == (nonce+1):
            B_req = self.create_request("",nonce=nonce+1)
            msg = B_req.encode()
            # msg = rsa.encrypt(msg,self.keys["B"])
            self.B_sock.send(msg)
            print("Sent ack to B")
        else:
            print("Oops there was a problem")
            self.B_sock.close()
            return 0
        return 1

    def communicate(self):

        nonce = 1

        for i in range(1,4):

            B_req = self.create_request("Hi "+str(nonce),nonce=nonce)
            msg = B_req.encode()
            # msg = rsa.encrypt(msg,self.keys["B"])
            self.B_sock.send(msg)
            print("Message sent to B")

            msg = self.B_sock.recv(MSG_SIZE)
            # msg = rsa.decrypt(msg, self.keys["private"])
            B_data = pickle.loads(msg)
            print("Message Received from ",B_data.sender," saying - ",B_data.request)

            nonce = B_data.nonce

        self.B_sock.close()




clientA = Client("A")
if clientA.getKey():
    clientA.communicate()



