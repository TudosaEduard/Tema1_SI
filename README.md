# Tema1_SI

Tema 1 la Securitatea Informației

Autor: Tudosă Eduard-Bogdan <br />
Prof. Coordonator: Nică Anca-Maria 

## Mediul de lucru

Codul a fost realizat in limbajul de programare Python(ide = PyCharm), utilizand libraria criptografica PyCryptodome. <br />

Pentru instalarea celor necesare si evitarea eventualelor erori:
* Windows PowerShell:
  * Run as administrator
  * Introduceti comanda: Set-ExecutionPolicy Unrestricted
  * Iesiti si intrati in PyCharm
* Intrati in proiect, in terminal si scrieti urmatoarele comenzi:
  * venv/Scripts/activate
  * pip install pycryptodome
  * pip install crypto
  * pip install aes

Astfel se vor evita erorile de instalare a pachetelor Crypto si AES necesare.

## Modul de rezolvare a temei

Cerinta problemei: [tema_1_SI .pdf](https://github.com/TudosaEduard/Tema1_SI/files/7379324/tema_1_SI.pdf) <br />

Informatiile teoretice se pot gasi aici:
 * https://profs.info.uaic.ro/~eonica/isec/index.html
 * https://profs.info.uaic.ro/~nica.anca/is.html <br />

Explicatii referitoare la comunicarea intre noduri si rezolvarea cerintei:
 * Nodul Generator:
   * Un nod suplimentar care va genera random cheia initiala si vectorul de initializare (cunoscute de toate nodurile implicate)
   * Acestea sunt pe 128 biti si vor fi trimise celor 3 noduri (A, B, MC) <br />
 * Nodul MC:
   * Preia cheia K si vectorul de initializare IV de la nodul Generator
   * Cripteaza cele 2 chei k1(specific modului de operare ECB) si k2(specific modului de operare CFB)
   * Comunica cele 2 chei criptate nodurilor A si B, la cerinta acestora <br />
 * Nodul A:
   * Preia cheia K si vectorul de initializare IV de la nodul Generator
   * Trimite mesaj catre MC pentru a cere una din cheile k1 sau k2(in functie de modul de operare dorit)
   * Decripteaza cheia preluata de la nodul MC
   * Cripteaza mesajul cu cheia decriptata si eventual vectorul de initializare(in functie de modul de operare dorit)
   * Specifica nodului B modul de operare in care va fi criptat mesajul
   * Dupa confirmarea comunicarii de catre nodul B, trimitem mesajul criptat lui B <br />
 * Nodul B:
   * Preia cheia K si vectorul de initializare IV de la nodul Generator
   * Asteapta mesajul referitor la modul de comunicare de la nodul A
   * Trimite mesaj catre MC pentru a cere una din cheile k1 sau k2(in functie de modul de operare dorit de nodul A)
   * Decripteaza cheia preluata de la nodul MC
   * Confirma nodului A ca poate primi mesajul
   * Preia de la nodul A mesajul criptat
   * Decripteaza mesajul cu cheia decriptata si eventual vectorul de initializare(in functie de modul de operare dorit de nodul A)

## Modul de comunicare intre noduri

Comunicarea se realizeaza in retea.

Ordinea de rulare a nodurilor este: Generator.py, MC.py, A.py, B.py

A se observa comunicarea intre noduri in consola.

## Teste efectuate si observatii

In urma testelor efectuate, am observat faptul ca algoritmii de criptarile/decriptarile din libraria PyCryptodome au oferit ceea ce trebuia. <br />
Rezultatele de criptare/decriptare pot fi observate in console la rularea nodurilor. <br />
De precizat faptul ca au fost probleme in ceea ce priveste padding-ul, rezolvate ulterior cu ajutorul instructiunilor pad,unpad din pachetul Crypto <br />
Rezultatul a fost verificat in urma potrivirilor de text din fisierele mesaj.txt si mesaj_decriptat.txt.
