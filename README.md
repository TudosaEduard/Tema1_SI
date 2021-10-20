# Tema1_SI

Tema 1 la Securitatea Informației

Autor: Tudosă Eduard-Bogdan <br />
Prof. Coordonator: Nică Anca-Maria 

## Mediul de lucru

Codul a fost realizat în limbajul de programare Python(ide = PyCharm), utilizând librăria criptografică PyCryptodome. <br />

Pentru instalarea celor necesare și evitarea eventualelor erori:
* Windows PowerShell:
  * Run as administrator
  * Introduceți comanda: Set-ExecutionPolicy Unrestricted
  * Ieșiți și intrați în PyCharm
* Intrați în proiect, în terminal și scrieți urmatoarele comenzi:
  * venv/Scripts/activate
  * pip install pycryptodome
  * pip install crypto
  * pip install aes

Astfel se vor evita erorile de instalare a pachetelor Crypto și AES necesare.

## Modul de rezolvare a temei

Cerința problemei: [tema_1_SI .pdf](https://github.com/TudosaEduard/Tema1_SI/files/7379324/tema_1_SI.pdf) <br />

Informațiile teoretice se pot găsi aici:
 * https://profs.info.uaic.ro/~eonica/isec/index.html
 * https://profs.info.uaic.ro/~nica.anca/is.html <br />

Explicații referitoare la comunicarea între noduri și rezolvarea cerintei:
 * Nodul Generator:
   * Un nod suplimentar care va genera random cheia inițială și vectorul de inițializare (cunoscute de toate nodurile implicate)
   * Acestea sunt pe 128 biți și vor fi trimise celor 3 noduri (A, B, MC) <br />
 * Nodul MC:
   * Preia cheia K și vectorul de inițializare IV de la nodul Generator
   * Criptează cele 2 chei k1(specific modului de operare ECB) și k2(specific modului de operare CFB)
   * Comunică cele 2 chei criptate nodurilor A și B, la cerința acestora <br />
 * Nodul A:
   * Preia cheia K și vectorul de inițializare IV de la nodul Generator
   * Trimite mesaj către MC pentru a cere una din cheile k1 sau k2(în funcție de modul de operare dorit)
   * Decriptează cheia preluată de la nodul MC
   * Criptează mesajul(pe blocuri de câte 128 biți) cu cheia decriptată și eventual vectorul de inițializare(în funcție de modul de operare dorit)
   * Specifică nodului B modul de operare în care va fi criptat mesajul
   * Dupa confirmarea comunicării de către nodul B, trimitem mesajul criptat lui B <br />
 * Nodul B:
   * Preia cheia K și vectorul de inițializare IV de la nodul Generator
   * Asteaptă mesajul referitor la modul de comunicare de la nodul A
   * Trimite mesaj către MC pentru a cere una din cheile k1 sau k2(în funcție de modul de operare dorit de nodul A)
   * Decriptează cheia preluată de la nodul MC
   * Confirmă nodului A că poate primi mesajul
   * Preia de la nodul A mesajul criptat
   * Decriptează mesajul(pe blocuri de câte 128 biți) cu cheia decriptată și eventual vectorul de inițializare(în funcție de modul de operare dorit de nodul A)

## Modul de comunicare între noduri

Comunicarea se realizează în rețea.

Ordinea de rulare a nodurilor este: Generator.py, MC.py, A.py, B.py

A se observa comunicarea între noduri in consola.

## Teste efectuate si observatii

În urma testelor efectuate, am observat faptul că algoritmii de criptare/decriptare din librăria PyCryptodome au oferit ceea ce trebuia.

Rezultatele de criptare/decriptare pot fi observate în console la rularea nodurilor.

De precizat faptul că au fost probleme în ceea ce priveste padding-ul, rezolvate ulterior cu ajutorul instrucțiunilor pad și unpad din pachetul Crypto.

Rezultatul a fost verificat în urma potrivirilor de text din fisierele mesaj.txt și mesaj_decriptat.txt.
