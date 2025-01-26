import socket
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Conexiune:
    def __init__(self, sock, host, server):
        # Creeaza un socket de comunicare
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Deschide conexiunea pe tuplul (port, ip)
        self.sock.bind(host)

        self.sock.connect(server)

        # Initializeaza datele conexiunii
        self.clientSocket = None
        self.addr = None

        # Initializeaza cheile
        key = RSA.generate(2048)
        self.privateKey = key
        self.publicKey = key.publickey().export_key(format='PEM')
        self.publicServerKey = None

    def SchimbDeCheiPublice(self):
        self.sock.sendall(self.publicKey)
        while True:
            buff = self.sock.recv(4096)
            if len(buff) < 4096:
                break
        
        self.publicServerKey = RSA.import_key(buff)

    def ConstruiesteMesaj(self, msg):
        # Transofrma in bytes
        encodedMsg = msg.encode()

        # Aplica SHA-256
        hash = SHA256.new(encodedMsg)

        # Cripteaza mesajul cu cheia publica a serverului
        cifru = pkcs1_15.new(self.privateKey).sign(hash)

        # Trimite mesaj
        self.sock.sendall(encodedMsg + b'--SEMNATURA--' + cifru)

    def TrimiteFisier(self, specie):

        filePath = "../Model/" + specie + ".pt"

        with open(filePath, 'rb') as file:
            while True:
                data = file.read(1024)
                if len(data) == 0:
                    break
                # Trimite mesaj
                self.sock.sendall(data)
        print("am iesit")
        # Primeste raspuns
        self.sock.close()
