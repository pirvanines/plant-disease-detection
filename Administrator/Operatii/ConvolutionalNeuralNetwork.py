import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()

        self.cnn_model = nn.Sequential(
            nn.Conv2d(in_channels = 3, out_channels = 6, kernel_size = (5,5)),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size = 2, stride = 5),
            nn.Conv2d(in_channels = 6, out_channels = 16, kernel_size = (5,5)),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size = 2, stride = 5),
            nn.Conv2d(in_channels = 16, out_channels = 20, kernel_size = (5,5)),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size = 2, stride = 2)
        )

        self.fully_connected_model = nn.Sequential(
            #nn.Linear(in_features = 720, out_features = 180), 
            #nn.Tanh(),
            nn.Linear(in_features = 180, out_features = 60),
            nn.Tanh(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features = 60, out_features = 16),
            nn.Tanh(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features = 16, out_features = 1)
        )

    def forward(self, images):
        images = self.cnn_model(images)
        images = images.view(images.size(0), -1)
        images = self.fully_connected_model(images)
        images = torch.sigmoid(images)

        return images
    

