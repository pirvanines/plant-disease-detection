from .abstractDataset import Dataset

import numpy as np
import glob
import cv2
from sklearn.model_selection import train_test_split

class Plante(Dataset):
    def __init__(self, pathS, pathB, mode):

        # Declara variable ce vor contine imaginile
        # de test si de validare
        self.X_train, self.Y_train, self.X_val, self.Y_val = None, None, None, None

        # Ca sa stiu cum am nevoie sa salvez datele
        self.mode = mode

        # Extrage imaginile din foldere
        planteBolnave = Plante.ExtrageImaginiDinFolder(pathB)
        planteSanatoase = Plante.ExtrageImaginiDinFolder(pathS)

        # ---------------------------- Images ------------------------------
        planteBolnave = np.array(planteBolnave, dtype = np.float32)
        planteSanatoase = np.array(planteSanatoase, dtype = np.float32)

        # ---------------------------- Labels ------------------------------
        labelPlanteBolnave = np.ones(planteBolnave.shape[0], dtype = np.float32)
        labelPlanteSanatoase = np.zeros(planteSanatoase.shape[0], dtype = np.float32)

        # -------------------------- Concatenare ---------------------------
        self.images = np.concatenate((planteBolnave, planteSanatoase), axis=0)
        self.labels = np.concatenate((labelPlanteBolnave, labelPlanteSanatoase), axis=0)

    def __getitem__(self, index):
        if self.mode == 'train':
            rezultat = {'image': self.X_train[index], 'label': self.Y_train[index]}
        elif self.mode == 'val':
            rezultat = {'image': self.X_val[index], 'label': self.Y_val[index]}
        elif self.mode == 'test':
            rezultat = {'image': self.images[index], 'label': self.labels[index]}
        return rezultat
    
    def __len__(self):
        # Numarul de imagini din datatset
        # in functie de modul in care ma aflu
        if self.mode == 'train':
            return self.X_train.shape[0]
        elif self.mode == 'val':
            return self.X_val.shape[0]
        elif self.mode == 'test':
            return self.images.shape[0]

    def ExtrageImaginiDinFolder(path):
        output = []

        for file in glob.iglob(path):

            # Extrage si redimensioneaza imaginea
            # la o dimensiune standard
            image = cv2.imread(file)
            image = cv2.resize(image, (256,256))
            
            # Reordoneaza canalele: BGR -> RGB
            B, G, R = cv2.split(image)
            image = cv2.merge([R, G, B])
            image = image.reshape((image.shape[2], image.shape[0], image.shape[1]))

            # Adauga imaginea in vector
            output.append(image)
        
        return output

    def TrainValidSplit(self):
        self.X_train, self.X_val, self.Y_train, self.Y_val = \
        train_test_split(self.images, self.labels, test_size = 0.20, random_state=42)
    
    def Normalizare(self):
        self.images = self.images/255.0
    