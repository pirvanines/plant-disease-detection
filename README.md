# Description

This is a web application designed to analyze the health status of a plant.

Requests are interpreted by the application server, and the plants it can analyze are determined by the training data configured by the administrator through the dedicated application.

The administrator application is responsible for training the neural network, generating configuration files, and updating the server-side data over the internet. To ensure data authenticity, RSA encryption was used.

# Purpose

This project provides a tool for identifying specific characteristics in images using convolutional neural networks (CNNs). It's functionality was proven by identifying the diseases affecting strawberry leaves.

# User Instructions

## Prerequisites ##

- Ensure that the path to this folder does not contain any spaces

- Create one virtual environment for Admin; check **Administrator/README.md**
- Create another virtual environment for Server; check **Server/README.md**

- To use this app, enter the IP address of the machine on which the server will run:
    - **Web/js/script.js:** line 1
    - **Administrator/Interfata/interfata.py:** line 7



## Running the Application ##

### Server:
- Open a Command Prompt (CMD) window with administrator privileges
- Activate the server's virtual environment
- Run the server's main execution file: **Server/server.py**

### Administrator:
- Open a Command Prompt (CMD) window with administrator privileges
- Activate the administrator's virtual environment
- Run the administrator application's main execution file: **Administrator/Interfata/interfata.py**

### Using the Application:
- Open a web browser and navigate to **http://IP:port/** to access and interact with the application
- Execute commands through the administrator interface using the available options.


