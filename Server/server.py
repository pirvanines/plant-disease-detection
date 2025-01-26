from web import ClientWeb
from admin import ClientAdmin

import threading
import time

pause_eventSS = threading.Event()
pause_eventCA = threading.Event()

def webThread():
    web_conn = ClientWeb('', 5678, 5)

    while True:

        print('#########################################################################')
        print('Serverul asculta potentiali clienti.')

        web_conn.AsteaptaConexiune()

        print('S-a conectat un client.')

        while pause_eventSS.is_set():
            pause_eventSS.wait()

        # Seteaza evenimentul de citire ca activ si pregatit
        pause_eventCA.set()

        command = web_conn.GetCerere()

        print('S-a citit linia de start din cerere: ##### ' + command + ' #####')

        if command != '':
            web_conn.InterpreteazaCerere(command)

        print('S-a terminat comunicarea cu clientul.')

        # Seteaza evenimentul de citire ca inactiv
        pause_eventCA.clear()


def adminThread():
    admin_conn = ClientAdmin('', 5679, 5)
    status = 1
    while True:
        # Asculta pe portul 5679 cereri
        admin_conn.AsteaptaConexiune()
        print("S-a conectat administratorul")

        # Verifica autenticitatea administratorului 
        admin_conn.SchimbDeCheiPublice()
        status = admin_conn.GetCerere()

        # Daca administatorul este cine pretinde ca este
        if status == 0:
            while pause_eventCA.is_set():
                # Asteapta ca ultima cerere a clientului web sa se termine
                pause_eventCA.wait()
            
            print('Incepe scrierea')

            # Seteaza evenimentul de scriere ca activ si pregatit
            pause_eventSS.set()

            admin_conn.PrimesteFisier()

            print("S-a primit fisierul de configurare")
            
            # Seteaza evenimentul de scriere ca inactiv
            pause_eventSS.clear()

            print('#########################################################################')
            print('Serverul asculta potentiali clienti.')
        else:
            print("Acesta nu este un administrator")

def main():

    pause_eventCA.clear()
    pause_eventSS.clear()

    thread1 = threading.Thread(target = webThread)
    thread2 = threading.Thread(target = adminThread)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == '__main__':
    main()