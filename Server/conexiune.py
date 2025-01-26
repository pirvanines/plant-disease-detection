import socket

class Conexiune:
    def __init__(self, ip, port, numOfClients):
        # Creeaza un socket de comunicare
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Deschide conexiunea pe tuplul (port, ip)
        self.sock.bind((ip, port))

        # Se specifica cati clienti pot astepta preluarea conexiunii
        self.sock.listen(numOfClients)

        # Initializeaza datele conexiunii
        self.clientSocket = None
        self.addr = None

    def AsteaptaConexiune(self):
        # Identifica clientul care vrea sa se conecteze
        (self.clientSocket, self.addr) = self.sock.accept()

