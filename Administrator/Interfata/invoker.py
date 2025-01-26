import tkinter as tk
from tkinter import messagebox

from operations import Evaluate, Train, ActualizeazaServer

class Invoker():
    def __init__(self):
        self.operation = None 

    def SetOperation(self, operation):
        self.operation = operation

    def ExecuteCommand(self):
        err = self.operation.CheckParameters()

        if err == 0:
            self.operation.Execute()

    