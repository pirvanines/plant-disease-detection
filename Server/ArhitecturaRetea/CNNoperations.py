from .ConvolutionalNeuralNetwork import CNN

import numpy as np
import torch
import cv2
import os

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

class MyNeuralNetwork():
    def __init__(self, imagePath):
        # Seteaza calea catre imagine
        self.imagePath = imagePath

        # Aleg unde o sa fac operatiile: CPU sau GPU
        # cu preferinta pentru GPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = CNN().to(self.device)

    def threshold(self, scoruri, threshold=0.5, min=0, max=1.0):
        values = np.array(list(scoruri))
        
        for index in range(len(values)):
            if values[index] > threshold:
                values[index] = max
            else:
                values[index] = min

        return values

    def test(self, specie):
        # Setez modelul ca si model de testare
        self.model.eval()

        # Incarca modelul
        self.model.load_state_dict(torch.load('./Model/'+specie+'.pt'))

        # Citeste imaginea ce se doreste a fi testata
        image = cv2.imread(self.imagePath)
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
    
    def detect_image(self, numeFisierPt, device=''):
        model_path = "./Model/" + numeFisierPt + ".pt"
        
        # Setare dispozitiv (GPU sau CPU)
        device = select_device(device)

        # Încărcarea modelului
        model = DetectMultiBackend(model_path, device=device)
        stride = model.stride
        img_size = 640  # Asumăm o dimensiune standard pentru YOLOv5

        # Încărcarea și preprocesarea imaginii
        dataset = LoadImages(self.imagePath, img_size=img_size, stride=stride, auto=True)

        # Pregătirea modelului pentru inferență
        model.warmup(imgsz=(1, 3, img_size, img_size))  # specific warmup

        # Rularea inferenței pe imagine
        for path, img, im0s, vid_cap, s in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.float() / 255.0  # scalare între 0.0 și 1.0
            if len(img.shape) == 3:
                img = img.unsqueeze(0)

            # Inferență
            pred = model(img)

            # Aplicarea Non-Max Suppression pentru a filtra predicțiile
            pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False)

            # Procesarea predicțiilor
            for i, det in enumerate(pred):  # Iterăm prin detectii
                if len(det):
                    # Rescalăm cutiile de la dimensiunea img la dimensiunea originală im0
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0s.shape).round()

                    # Afișăm rezultatele
                    for *xyxy, conf, cls in det:
                        if conf > 0.5:
                            #print(f'In imaginea data s-a gasit clasa: {model.names[int(cls)]}')
                            return (conf, model.names[int(cls)])
        return (0, 0)