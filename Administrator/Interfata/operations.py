import sys
import os
import tkinter as tk
from tkinter import messagebox
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command import Command
from check import Check
from Operatii.NeuralNetwork import MyNeuralNetwork
from conexiuneAdmin import Conexiune

class Train(Command):
    def __init__(self, console, specie, batch, epoch):
        self.checker = Check()
        
        self.eta = 0.0001
        self.pathToData = '../Dataset/'
        self.pathToModel = '../Model/speciePlante.pt'
        self.NN = MyNeuralNetwork(self.eta)

        self.pathS = self.pathToData + specie + "/yes/*.jpg"
        self.pathB = self.pathToData + specie + "/no/*.jpg"

        self.specie = specie
        self.batch = batch
        self.epoch = epoch

        self.console = console

    def CheckParameters(self):
        if self.checker.CheckSpecies(self.specie) == 0:
                if self.checker.CheckBatch(self.batch) == 0:
                    err = self.checker.CheckEpochs(self.epoch)

                    if err == 1:
                        raspuns = messagebox.askyesno("Avertisment", f"Esti sigur ca vrei sa antrenezi cu {self.epoch} epoci?")
                        if raspuns:
                            err = 0
                    elif err == 2:
                        messagebox.showerror("Eroare", "Numarul de epoci trebuie sa fie un numar pozitiv!")
                    
                    return err
                
                else:
                    messagebox.showerror("Eroare", "Batch size trebuie sa fie un intreg intre 0 si 32")
        else:
            messagebox.showerror("Eroare", "Specia introdusa nu este recunoscuta de model")
        return 2
    
    def Execute(self):
        self.NN.train(self.console, self.epoch, self.pathS, self.pathB, self.batch, self.specie, 'train')
    
class Evaluate(Command):
    def __init__(self, console, specie):
        self.checker = Check()

        self.pathToData = '../Dataset/'
        self.pathToModel = '../Model/speciePlante.pt'

        self.pathS = self.pathToData + specie + "/yes/*.jpg"
        self.pathB = self.pathToData + specie + "/no/*.jpg"

        self.eta = 0.0001
        self.NN = MyNeuralNetwork(self.eta)

        self.specie = specie

        self.console = console

    def CheckParameters(self):
        err =  self.checker.CheckSpecies(self.specie)
        if err == 2:
            messagebox.showerror("Eroare", "Specia introdusa nu este recunoscuta de model")
        return err

    def Execute(self):
        self.NN.evaluate(self.console, self.pathS, self.pathB, 32, self.specie, 'val')

class ActualizeazaServer(Command):
    def __init__(self, sock, console, ip, port, specie, trainButton, evaluateButton):
        self.check = None
        
        self.console = console
        self.specie = specie

        self.trainButton = trainButton
        self.evaluateButton = evaluateButton

        self.validIP = self.GetOwnIP()
        if self.validIP != "1":
            ip_host = self.validIP

            host = (ip_host, 4000)
            server = (ip, port)

            self.conn = Conexiune(sock, host, server)
        else:
            messagebox.showerror("Eroare", "Nu s-a gasit adresa IP a masinii gazda")


    def CheckParameters(self):
        if self.validIP != "1":
            return 0
        return 1
    
    def Execute(self):
        self.trainButton.config(state = tk.DISABLED)
        self.evaluateButton.config(state = tk.DISABLED)

        self.conn.SchimbDeCheiPublice()
        self.conn.ConstruiesteMesaj("update")
        self.conn.TrimiteFisier(self.specie)

        self.trainButton.config(state = tk.NORMAL)
        self.evaluateButton.config(state = tk.NORMAL)
        messagebox.showinfo("Info", "Conexiune cu serverul realizata cu succes. S-a trimis modelul retelei neuronale")

    def GetOwnIP(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return "1"