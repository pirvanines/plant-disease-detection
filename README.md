# Descriere

Aceasta este o aplicatie web ce are ca scop analiza starii de sanatate a unei plante.

Cererile sunt interpretate de serverul aplicatiei, iar plantele pe care le poate analiza acesta sunt determinate de datele de antrenare setate de administrator din aplicatia dedicata.

La nivelul aplicatiei administrator se realizeaza antrenarea retelei neuronale, generarea fisierelor de configurare si actualizarea datelor la nivel de server prin internet. Pentru a asigura autenticitatea datelor, am realizat criptarea datelor cu RSA.

# Scop

Scopul acestui proiect este de a pune la dispozitia utilizatorilor o unealta de identificare a anumitor caracteristici in imagini cu ajutorul retelelor neuronale convolutionale. In cadrul acestui proiect am realizat un sudiu de caz asupra identificarii bolilor la frunzele de capsuna.

# Instructiuni de utilizare

## Cerințe preliminare ##

- Se va asigura ca path-ul pana la acest folder nu contine spatii

- Se va crea mediul virtual conform instructiunilor din folderul **Administrator/README.md**
- Se va crea mediul virtual conform instructiunilor din folderul **Server/README.md**

- Pentru utilizarea proiectului se vor modifica adresele IP in urmatoarele 2 fisiere:
    - **Web/js/script.js:** la inceputul fisierului (linia 1), se introduce ip-ul masinii unde se va rula serverul
    - **Administrator/Interfata/interfata.py:** la inceputul fisierului (linia 7) se modifica ip-ul masinii unde se va rula serverul




## Executia programului ##

### Server:
- se deschide o consola cmd cu drepturi de administrator
- Se activeaza mediul virtual al serverului
- se porneste fisierul de executie al serverului: **Server/server.py**

### Administrator:
- se activeaza mediul virtual al administratorului
- se porneste fisierul de executie al administratorului: **Administrator/Interfata/interfata.py**

### Executia:
- se acceseaza din browserul web http://IP:port/ si se navigheaza in aplicatie
- se executa comenzi din interfata administrator conform optiunilor puse la dispozitie

## Contributing

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
