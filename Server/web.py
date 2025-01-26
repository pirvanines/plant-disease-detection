from ArhitecturaRetea.CNNoperations import MyNeuralNetwork
from conexiune import Conexiune

import socket
import os
import gzip
from detect import detect_image
import openai

openai.api_key = "..."

class ClientWeb(Conexiune):
    def __init__(self, ip, port, numOfClients):

        # Deschide conexiunea pe portul 5678, de la orice IP
        super().__init__(ip, port, numOfClients)

        # Numele Serverului
        self.name = "Plant Disease Server"

        # Tipuri de fisiere ce pot fi cerute
        self.tipuriMedia = {
            'html': 'text/html; charset=utf-8',
            'css': 'text/css; charset=utf-',
            'js': 'text/javascript; charset=utf-8',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'ico': 'image/x-icon',
            'xml': 'application/xml; charset=utf-8',
            'json': 'application/json; charset=utf-8'
        }

        # Configuratia retelei neuronale
        current_path = os.getcwd()
        photo_path = current_path + "\\Photo\\photo.jpg"
        self.retea = MyNeuralNetwork(photo_path)

        # GPT model
        self.GPTmodel ="gpt-4-turbo"


    def AsteaptaConexiune(self):
        super().AsteaptaConexiune()
    
    def GetCerere(self):
        req = b""
        buffer = b""
        command = ''

        while True:
            # Primeste mesaj
            buffer = self.clientSocket.recv(2048)

            # Decodifica octetii
            #req = req + buff.decode()
            req += buffer

            print(len(buffer))

            if b'\r\n\r\n' in req:
                headers, body = req.split(b'\r\n\r\n', 1)
                if b'POST' in headers:
                    if b'Content-Length:' in headers:
                        content_length = int(headers.split(b'Content-Length:')[1].split(b'\r\n')[0].strip())
                        if len(body) >= content_length:
                            break
                else:
                    if len(buffer) < 2048:
                        break

        if req == b'':
            self.clientSocket.close()
            return ''
        
        else:
            headers = req.split(b'\r\n')
            method, path, _ = headers[0].split(b' ')

            if method == b'POST':
                header, body_raw = req.split(b'\r\n\r\n', 1)
                #print(req)
                self.SalvareImagine(header, body_raw)
                
                command = headers[0].decode('utf-8')


            # Daca sirul de date este valid
            # extrage comanda si iese din bucla de ascultare
            if (method == b'GET' and command == ''):
                command = headers[0].decode('utf-8')
                
            # Daca nu s-a primit nici o comanda
            # se incheie conexiunea
            if method == b'':
                self.clientSocket.close()

        return command
    
    def SalvareImagine(self, headers, body):
        try:
            #print(headers)
            
            #print(body)
            headers_dict = {}
            header_lines = headers.split(b'\r\n')
            for line in header_lines:
                if b': ' in line:
                    key, value = line.split(b': ', 1)
                    headers_dict[key.decode('utf-8')] = value.decode('utf-8')

            content_type = headers_dict['Content-Type']
            
            if content_type and content_type.startswith('multipart/form-data'):
                boundary = content_type.split('boundary=')[-1].encode()
                parts = body.split(b'--' + boundary + b'\r\n')

                
                for part in parts:
                    if not part or part == b'--\r\n':
                        continue
                    
                    part_headers, part_body = part.split(b'\r\n\r\n', 1)

                    #print(part_headers)
                    
                    part_headers_dict = {}
                    header_lines = part_headers.split(b'\r\n')
                    for line in header_lines:
                        if b': ' in line:
                            key, value = line.split(b': ', 1)
                            part_headers_dict[key.decode('utf-8')] = value.decode('utf-8')
                        
                    with open('.\\Photo\\photo.jpg', 'wb') as f:
                        f.write(part_body.rstrip(b'\r\n--' + boundary + b'--\r\n'))
                        #return 0
        except IOError:
            # Se initializeaza resursa
            buff = ('Eroare la procesarea cererii').encode("utf-8")

            # Dimensiunea resursei
            contentLength = str(len(buff))

            # Se trimite raspuns 404 Not Found
            self.SendResponse('404 Not Found', contentLength, 'text/plain; charset=utf-8', 'gzip')

            # Se trimite resursa
            self.clientSocket.sendall(gzip.compress(buff))

            # Se incheie conexiunea
            self.clientSocket.close()

        #return 1

    def InterpreteazaCerere(self, command):
        elemCommand = command.split()
        header = elemCommand[1]
        op = elemCommand[0]
        
        #print(header)
        #print(op)

        if op == 'GET':
            resursa = header.replace("/", "\\")
            self.GetResursa(resursa)
        elif op == 'POST':
            if header.find(".jpg"):
                self.Analize()
            

    def GetResursa(self, numeResursa):
        if(numeResursa == '\\'):
            numeResursa = '\\index.html'

        # Construieste calea catre resursa
        currentPath = os.getcwd()
        pathToResource = os.path.dirname(currentPath) + '\\Web' + numeResursa

        print(pathToResource)

        # Incearca sa acceseze resursa
        buff = None
        file = None
        try:
            # Deschide fisierul pentru citire (binar)
            file = open(pathToResource, 'rb')

            # Tip media cerut
            extensie = pathToResource[pathToResource.rfind('.') + 1:]
            tipMedia = self.tipuriMedia.get(extensie, 'text/plain; charset=utf-8')

            # Dimensiunea resursei
            contentLength  =str(os.stat(pathToResource).st_size)

            # Se trimite raspunsul 200 OK
            self.SendResponse('200 OK', contentLength, tipMedia, 'gzip')

            # Se initializeaza resursa
            buff = file.read()
        
        except IOError:
            # Se initializeaza resursa
            buff = ('Eroare! Resursa ceruta ' + numeResursa + ' nu a putut fi gasita!').encode("utf-8")

            # Dimensiunea resursei
            contentLength = str(len(buff))

            # Se trimite raspuns 404 Not Found
            self.SendResponse('404 Not Found', contentLength, 'text/plain; charset=utf-8', 'gzip')

        finally:
            if file is not None:
                file.close()

        # Se trimite resursa
        self.clientSocket.sendall(gzip.compress(buff))

        # Se incheie conexiunea
        self.clientSocket.close()

    def Analize(self):

        current_path = os.getcwd()
        model_path = current_path + "\\Model\\speciePlante.pt"

        conf, nume = self.retea.detect_image("speciePlante")

        #model_disease_path = current_path + "\\Model\\capsuna"

        buff = ''
        rezultat = ''
        # Se initializeaza resursa
        if conf:
            result = self.retea.test("capsuna")
            user_prompt = ""
            if result == 0:
                rezultat = ("S-a gasit planta {} sanatoasa.".format(nume))
                user_prompt = "Scrie-mi trei sau patru propozitii despre ingrijirea plantei: " + nume
                
            elif result == 1:
                rezultat = ("S-a gasit planta {} bolnava.".format(nume))
                user_prompt = "Scrie-mi trei sau patru propozitii despre bolile plantei: " + nume
            
            chatbot_response = self.GetInfoAboutPlant(user_prompt)
            buff = ("S-a analizat cu succes. " + rezultat + " "+chatbot_response).encode("utf-8")
        else:
            buff = ("S-a analizat cu succes. In imagine nu se gaseste o planta cunoscuta de modelul nostru...:(").encode("utf-8")
        
        # Dimensiunea resursei
        contentLength = str(len(buff))

        # Se trimite raspuns 404 Not Found
        self.SendResponse('200 OK', contentLength, 'text/plain; charset=utf-8', 'gzip')

        # Se trimite resursa
        self.clientSocket.sendall(gzip.compress(buff))

        # Se incheie conexiunea
        self.clientSocket.close()

    def SendResponse(self, status, cl, ct, ce):
        self.clientSocket.sendall(('HTTP/1.1 '+ status +'\r\n').encode("utf-8"))
        self.clientSocket.sendall('Access-Control-Allow-Origin: *\r\n'.encode("utf-8"))
        self.clientSocket.sendall(('Content-Length: ' + cl + '\r\n').encode("utf-8"))
        self.clientSocket.sendall(('Content-Type: ' + ct + '\r\n').encode("utf-8"))
        self.clientSocket.sendall(('Content-Encoding: ' + ce + '\r\n').encode("utf-8"))
        self.clientSocket.sendall(('Server: '+ self.name + '\r\n').encode("utf-8"))
        self.clientSocket.sendall('\r\n'.encode("utf-8"))

    def SendMessage(self, buffer):
        # Se trimite resursa
        self.clientSocket.sendall(gzip.compress(buffer))

        # Se incheie conexiunea
        self.clientSocket.close()

    def GetInfoAboutPlant(self, cerere):
        response = openai.ChatCompletion.create(
            model=self.GPTmodel,
            messages=[
                {"role": "user", "content": cerere}
            ]
        )
        message = response['choices'][0]['message']['content']
        return message
            




    
    





