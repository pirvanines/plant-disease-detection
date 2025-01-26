from conexiune import Conexiune
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class ClientAdmin(Conexiune):
    def __init__(self, ip, port, numOfClients):

        # Deschide conexiunea pe portul 5679, de la orice IP
        super().__init__(ip, port, numOfClients)

        # Initializeaza cheile
        key = RSA.generate(2048)
        self.privateKey = key
        self.publicKey = key.publickey().export_key(format='PEM')
        self.publicClientKey = None


    def AsteaptaConexiune(self):
        super().AsteaptaConexiune()

    def SchimbDeCheiPublice(self):
        while True:
            buff = self.clientSocket.recv(4096)

            if len(buff) < 4096:
                break
            
        self.publicClientKey = RSA.import_key(buff)
        self.clientSocket.sendall(self.publicKey)

    def GetCerere(self):
        while True:
            buffer = self.clientSocket.recv(1024)

            if buffer:
                # Separa mesajul de semnatura
                mesaj, semnatura = buffer.split(b'--SEMNATURA--')

                # Calculeaza hash-ul mesajului in plain text
                hash = SHA256.new(mesaj)

                # Verifica daca ce am codificat cu RSA este acelasi
                # cu hash-ul calculat anterior
                try:
                    pkcs1_15.new(self.publicClientKey).verify(hash, semnatura)
                    return 0
                except (ValueError, TypeError):
                    self.clientSocket.close()
                    return 1

            if len(buffer) < 1024:
                break

        return 1
    
    def PrimesteFisier(self):
        print("Se va primi fisierul")
        with open('./Model/capsuna.pt', 'wb') as file:
            while True:
                buffer = self.clientSocket.recv(1024)
                if len(buffer) < 1024:
                    break
                file.write(buffer)
        
        self.clientSocket.close()
        print('Fisier actualizat')
