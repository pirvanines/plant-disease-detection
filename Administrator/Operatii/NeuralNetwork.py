from .dataset import Plante
from .ConvolutionalNeuralNetwork import CNN
from .database import Databse

import numpy as np
import torch
import cv2
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns
import tkinter as tk
from tkinter import messagebox


class MyNeuralNetwork():
    def __init__(self, eta):

        # Setez pe None campurile ce vor fi
        # initializate mai tarziu
        self.database = None
        self.specie = None
        self.plante = None
        self.train_dataloader = None
        self.val_dataloader = None

        # Aleg unde o sa fac operatiile: CPU sau GPU
        # cu preferinta pentru GPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = CNN().to(self.device)

        # Optimizator entru antrenare
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = eta)

    def loadDatasets(self, pathS, pathB, batchSize, plantName, mode):
        # Initializez baza de date
        self.database = Databse("CNN", plantName)
        self.specie = plantName

        # Incarc imaginile din folder
        self.plante = Plante(pathS, pathB, mode)
        self.plante.Normalizare()
        self.plante.TrainValidSplit()

        # Creez grupurile de imagini care vor deservi la antrenare
        # sau la testare
        self.train_dataloader = DataLoader(self.plante, batch_size = batchSize, shuffle=True)
        self.val_dataloader = DataLoader(self.plante, batch_size = batchSize, shuffle=False)

    def threshold(self, scoruri, threshold=0.5, min=0, max=1.0):
        values = np.array(list(scoruri))
        
        for index in range(len(values)):
            if values[index] > threshold:
                values[index] = max
            else:
                values[index] = min

        return values

    # Ploteaza un grafic pentru len(inputVect) seturi de rezultate
    def PlotResult(self, inputVect, label):
        plt.figure(figsize=(16,9))
        inputLabels = ["Test "+label, "Validation "+label]
        for index in range(len(inputVect)):
            plt.plot(inputVect[index], label = inputLabels[index])

        plt.legend()
        plt.grid()
        plt.xlabel("Epochs", fontsize=20)
        plt.ylabel(label, fontsize=20)
        plt.show()

    def train(self, consola, epochs, pathS, pathB, batchSize, plantName, mode):
        # Incarca datele necesare antrenarii
        self.loadDatasets(pathS, pathB, batchSize, plantName, mode)

        # Va retine media pierderilor
        # pentru fiecare epoca
        epoch_train_loss = []
        epoch_val_loss = []

        epoch_train_accuracy = []
        epoch_val_accuracy = []

        # Incepe antrenarea
        for epoch in range(0, epochs):

            # -------------------------- Train -------------------------
            pierderi_train = []
            y_true_train = []
            outputs_train = []

            # Seteaza modul
            self.model.train()
            
            # Seteaza modul de extragere al datelor
            self.plante.mode = 'train'

            for data in self.train_dataloader:
                # Resetarea optimizerului -> sa nu
                # contina ceva in cache
                self.optimizer.zero_grad()

                # Incarcarea batch-ului de date
                image = data['image'].to(self.device)
                label = data['label'].to(self.device)

                # Predictia modelului -> trecerea prin retea
                y_hat = self.model(image)

                # Salveaza iesirile din terecerea prin retea
                outputs_train.append(y_hat.cpu().detach().numpy())
                y_true_train.append(label.cpu().detach().numpy())

                # Functia de pierderi
                error = nn.BCELoss()
                loss = torch.sum(error(y_hat.squeeze(), label))
                loss.backward()
                self.optimizer.step()

                # adaug la vectorul de pierderi pierderea
                # de la iteratia curenta
                pierderi_train.append(loss.item())
        
            # Pune iesirile functiei sigmoide intr-un vector unidimensional
            outputs_train = np.concatenate(outputs_train, axis=0).squeeze()
            y_true_train = np.concatenate(y_true_train, axis=0).squeeze()

            # Adauga performantele epocii
            epoch_train_loss.append(np.mean(pierderi_train))
            epoch_train_accuracy.append(accuracy_score(y_true_train,self.threshold(outputs_train)))

            # -------------------------- Validate -------------------------
            val_loss = []
            y_true_val = []
            outputs_val = []

            # Seteaza modul
            self.model.eval()

            # Seteaza modul de extragere al datelor
            self.plante.mode = 'val'

            with torch.no_grad():
                for data in self.val_dataloader:
                    # Incarcarea batch-ului de date
                    image = data['image'].to(self.device)
                    label = data['label'].to(self.device)

                    # Predictia modelului
                    y_hat = self.model(image)

                    # Salveaza iesirile din terecerea prin retea
                    outputs_val.append(y_hat.cpu().detach().numpy())
                    y_true_val.append(label.cpu().detach().numpy())

                    # Functia de pierderi
                    error = nn.BCELoss()
                    loss = torch.sum(error(y_hat.squeeze(), label))

                    val_loss.append(loss.item())

            # Pune iesirile functiei sigmoide intr-un vector unidimensional
            outputs_val = np.concatenate(outputs_val, axis=0).squeeze()
            y_true_val = np.concatenate(y_true_val, axis=0).squeeze()

            # Adauga performantele epocii
            epoch_val_loss.append(np.mean(val_loss))
            epoch_val_accuracy.append(accuracy_score(y_true_val,self.threshold(outputs_val)))

            # -------------------------- Prind Data -------------------------
            consola.insert(tk.END, 'For epoch {}:\n\ttrain loss is: {:.6f}\n\tval loss is: {:.6f}\n'.format(epoch, np.mean(pierderi_train), np.mean(val_loss)))

        # Calculeaza parametri de performanta ai modelului
        start_index = int(len(epoch_val_loss) * 3 / 4)

        media_train_loss = np.mean(epoch_train_loss[start_index:])
        media_val_loss = np.mean(epoch_val_loss[start_index:])

        media_train_acuratete = np.mean(epoch_train_accuracy[start_index:])
        media_val_acuratete = np.mean(epoch_val_accuracy[start_index:])

        acuratete = (media_train_acuratete + media_val_acuratete) / 2
        overfitFactor = abs(media_train_loss - media_val_loss)

        filtru = {"specie":self.specie}
        currentModelData = self.database.FindElement(filtru)

        # Pune datele modelului curent intr-un dictionar
        data = {
            "specie": self.specie,
            "batch" : batchSize,
            "epoci" : epochs,
            "acuratete": acuratete,
            "overfitFactor": overfitFactor,
        }


        if currentModelData != None:
            # Daca modelul curent este mai bun decat cel mai bun de pana acum
            if currentModelData["acuratete"] < acuratete and currentModelData["overfitFactor"] > overfitFactor:
                
                # Sterge elementul anterior din Mongo si insereaza datele noi
                self.database.DeleteElement(filtru)
                self.database.InsertDocument(data)

                # Suprascrie fisierul care contine modelul retelei
                torch.save(self.model.state_dict(), '../Model/'+self.specie+'.pt')
        else:
            # Salveaza datele curente in Mongo DB
            self.database.InsertDocument(data)
            
            # Suprascrie fisierul care contine modelul retelei
            torch.save(self.model.state_dict(), '../Model/'+self.specie+'.pt')


        consola.insert(tk.END, 'Acuratetea modelului este: {}\n'.format(acuratete))
        #print(currentModelData["acuratete"])
        #print(acuratete)

        consola.insert(tk.END, 'Factorul de overfit este: {}\n'.format(overfitFactor))
        #print(currentModelData["overfitFactor"])
        #print(overfitFactor)

        resultsVect_loss = []
        resultsVect_loss.append(epoch_train_loss)
        resultsVect_loss.append(epoch_val_loss)
        self.PlotResult(resultsVect_loss, "Loss")

        resultsVect_accuracy = []
        resultsVect_accuracy.append(epoch_train_accuracy)
        resultsVect_accuracy.append(epoch_val_accuracy)
        self.PlotResult(resultsVect_accuracy, "Accuracy")
    

    def test(self, path, specie):

        # Setez modelul ca si model de testare
        self.model.eval()

        # Incarca modelul
        self.model.load_state_dict(torch.load('../Model/'+specie+'.pt'))

        # Citeste imaginea ce se doreste a fi testata
        image = cv2.imread(path)
        image = cv2.resize(image, (256,256))

        # Reordoneaza canalele: BGR -> RGB
        B, G, R = cv2.split(image)
        image = cv2.merge([R, G, B])
        image = image.reshape((image.shape[2], image.shape[0], image.shape[1]))

        image_array = []
        image_array.append(image)

        with torch.no_grad():
            image_tensor = np.array(image_array, dtype = np.float32)
            image_tensor = torch.tensor(image_tensor)

            # Pun imaginea convertita in tensor pe GPU
            image_tensor = image_tensor.to(self.device)

            # Predictia modelului
            y_hat = self.model(image_tensor)

            # convertirea vectorilor in np arrays
            output = y_hat.cpu().detach().numpy()

        result = self.threshold(output)
        return result[0][0]
            


    def evaluate(self, consola, pathS, pathB, batchSize, plantName, mode):

        # Incarca datele necesare antrenarii
        self.loadDatasets(pathS, pathB, batchSize, plantName, mode)

        # Setez modelul ca si model de testare
        self.model.eval()

        self.model.load_state_dict(torch.load('../Model/'+self.specie+'.pt'))

        outputs = []
        y_true = []

        # Seteaza modul de extragere al datelor
        self.plante.mode = 'val'

        # operste calcularea gradientilor
        with torch.no_grad():
            for data in self.val_dataloader:
                # Incarcarea batch-ului de date
                image = data['image'].to(self.device)
                label = data['label'].to(self.device)

                # Predictia modelului
                y_hat = self.model(image)

                # convertirea vectorilor in np arrays
                outputs.append(y_hat.cpu().detach().numpy())
                y_true.append(label.cpu().detach().numpy())

        # Pune iesirile functiei sigmoide intr-un vector unidimensional
        outputs = np.concatenate(outputs, axis=0).squeeze()
        y_true = np.concatenate(y_true, axis=0).squeeze()

        consola.insert(tk.END, 'Acuratetea retelei este: {}\n'.format(accuracy_score(y_true,self.threshold(outputs))))

        confusionMatrix = confusion_matrix(y_true, self.threshold(outputs))
        plt.figure(figsize=(16,9))

        ax = plt.subplot()
        sns.heatmap(confusionMatrix,annot=True,fmt='g',ax=ax)

        # labels, totle and ticks
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title('Confusion Matrix')
        ax.xaxis.set_ticklabels(['Sanatos', 'Bolnav'])
        ax.yaxis.set_ticklabels(['Sanatos', 'Bolnav'])

        plt.figure(figsize=(16,9))
        plt.plot(outputs)
        plt.axvline(x=len(self.plante), color='r',linestyle='--')
        plt.grid()

        plt.show()


