import tkinter as tk
import socket
from tkinter import messagebox
from invoker import Invoker
from operations import Evaluate, Train, ActualizeazaServer

serverIP = '192.168.1.7'
serverPort = 5679

class Interfata():
    def __init__(self):
        self.invoker = Invoker()

    def on_train_click(self):
        try:
            specie = str(self.entry_a.get())
            batch = int(self.entry_b.get())
            epoch = int(self.entry_c.get())

            self.invoker.SetOperation(Train(self.console_text,specie, batch, epoch))
            self.invoker.ExecuteCommand()
            
        except ValueError:
            messagebox.showerror("Eroare", "Te rog introdu specia, numarul de epoci si batch size")

    def on_eval_click(self):
        try:
            specie = str(self.entry_a.get())

            self.invoker.SetOperation(Evaluate(self.console_text, specie))
            self.invoker.ExecuteCommand()

        except ValueError:
            messagebox.showerror("Eroare", "Te rog introdu Specia")

    def on_about_click(self):
        messagebox.showinfo("Info", "Reteaua neuronala poate fi antrenata sa recunoasca daca sunt bolnave frunzele de capsune. Numele corect pentru numele speciei de introdus in consola este: capsuna")

    def on_update_click(self):
        self.invoker.SetOperation(ActualizeazaServer("", self.console_text, serverIP, serverPort, 'capsuna', self.button2, self.button3))
        self.invoker.ExecuteCommand()

    def run(self):
        # Crearea ferestrei principale
        self.root = tk.Tk()
        self.root.title("Administrator")

        # Crearea și plasarea titlului
        title_label = tk.Label(self.root, text="Detectia automata a afectiunilor la plante", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Crearea frame-urilor pentru fiecare coloană
        frame_left = tk.Frame(self.root, width=200, height=400)
        frame_middle = tk.Frame(self.root, width=400, height=400)
        frame_right = tk.Frame(self.root, width=200, height=400)

        frame_left.grid(row=1, column=0, sticky="nsew")
        frame_middle.grid(row=1, column=1, sticky="nsew")
        frame_right.grid(row=1, column=2, sticky="nsew")

        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=2, uniform="group1")
        self.root.grid_columnconfigure(2, weight=1, uniform="group1")

        # Configurarea primei coloane
        subtitle_label = tk.Label(frame_left, text="Actualizeaza Server", font=("Helvetica", 14))
        subtitle_label.pack(pady=10, anchor='center')

        button1 = tk.Button(frame_left, height=1, width=10, text="Actualizeaza", command=self.on_update_click)
        button1.pack(pady=5, anchor='center')

        container_left = tk.Frame(frame_left)
        container_left.pack(anchor='center')

        subtitle_label = tk.Label(container_left, text="Configurare retea", font=("Helvetica", 14))
        subtitle_label.pack(pady=10, anchor='center')

        self.button2 = tk.Button(container_left, height=1, width=10, text="Antreneaza", command=self.on_train_click)
        self.button2.pack(pady=5, anchor='center')

        self.button3 = tk.Button(container_left, height=1, width=10, text="Evalueaza", command=self.on_eval_click)
        self.button3.pack(pady=5, anchor='center')

        button4 = tk.Button(container_left, height=1, width=10, text="Info", command=self.on_about_click)
        button4.pack(pady=5, anchor='center')

        # Configurarea celei de-a doua coloane
        self.console_text = tk.Text(frame_middle, height=20, width=50)
        self.console_text.pack(pady=5)

        # Configurarea celei de-a treia coloane
        entry_label = tk.Label(frame_right, text="Introducere Date", font=("Helvetica", 14))
        entry_label.pack(pady=10, anchor='center')

        container_right = tk.Frame(frame_right)
        container_right.pack(anchor='center')

        specie = tk.Label(container_right, text="Specie:", font=("Helvetica", 10))
        specie.pack(pady=2, anchor='w')

        self.entry_a = tk.Entry(container_right)
        self.entry_a.pack(pady=5, anchor='w')

        epoci = tk.Label(container_right, text="Batch:", font=("Helvetica", 10))
        epoci.pack(pady=2, anchor='w')

        self.entry_b = tk.Entry(container_right)
        self.entry_b.pack(pady=5, anchor='w')

        batch = tk.Label(container_right, text="Epoci:", font=("Helvetica", 10))
        batch.pack(pady=2, anchor='w')

        self.entry_c = tk.Entry(container_right)
        self.entry_c.pack(pady=5, anchor='w')

        # Rularea buclei principale a interfeței
        self.root.mainloop()

if __name__ == "__main__":
    window = Interfata()
    window.run()