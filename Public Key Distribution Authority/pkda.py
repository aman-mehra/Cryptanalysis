import socket
import rsa
import pickle
from contextlib import closing
import ntplib
import signal
import sys


ntp_client = ntplib.NTPClient()
TIMEOUT = 100
PKDA_PORT = 2222
MSG_SIZE = 512


def load_keys():
    PU_A, PU_B, PU_PKDA, PR_PKDA = None,None,None,None

    with open('ClientA.pkl', 'rb') as f:
        d = pickle.load(f)
        PU_A = d["public"]
    with open('ClientB.pkl', 'rb') as f:
        d = pickle.load(f)
        PU_B = d["public"]
    with open('pkda.pkl', 'rb') as f:
        d = pickle.load(f)
        PU_PKDA = d["public"]
        PR_PKDA = d["private"]

    return PU_A, PU_B, PU_PKDA, PR_PKDA

class Packet:
    def __init__(self, sender, request, time, reply = None, nonce = 0):
        self.sender = sender
        self.request = request
        self.time = time
        self.reply = reply
        self.nonce = nonce
    def encode(self):
        return pickle.dumps(self)

class PKDA:

    def __init__(self, PU_A, PU_B, PU_PKDA, PR_PKDA):
        self.keys = {
            "private":PU_PKDA,
            "public":PR_PKDA,
            "A":PU_A,
            "B":PU_B
        }
        self.port = -1
        self.create_socket()


    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = PKDA_PORT
        self.port = PORT

        self.s.bind((HOST,self.port))
        self.s.listen()
        print("Pkda connected to port "+str(self.port))

    def run_key_sevice(self):
        
        # Query from A

        (clientsocket, address) = self.s.accept()
        data = pickle.loads(clientsocket.recv(MSG_SIZE))
        print("A request has been recvd - sender:",data.sender," request:",data.request,"time:",data.time)

        cur_time = ntp_client.request('uk.pool.ntp.org', version=3).tx_time 
        if cur_time - data.time < TIMEOUT:
            response = Packet("PKDA",data,cur_time,self.keys[data.request])
            msg = response.encode()
            msg = rsa.encrypt(msg, self.keys["private"])
            clientsocket.send(msg)
            print("Response Sent")

        # Query from B

        (clientsocket, address) = self.s.accept()
        data = pickle.loads(clientsocket.recv(MSG_SIZE))
        print("A request has been recvd - sender:",data.sender," request:",data.request,"time:",data.time)

        cur_time = ntp_client.request('uk.pool.ntp.org', version=3).tx_time 
        if cur_time - data.time < TIMEOUT:
            response = Packet("PKDA",data,cur_time,self.keys[data.request])
            msg = response.encode()
            # msg = rsa.encrypt(msg, self.keys["private"])
            clientsocket.send(msg)
            print("Response Sent")


        
pkda = PKDA(*load_keys())
pkda.run_key_sevice()





