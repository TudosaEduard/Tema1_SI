import socket
import random
import string

from Crypto.Cipher import AES

# Porneste discutia cu generatorul pentru a lua cheia si vectorul de initializare


def generator_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 111

    s.connect((host, port))
    K = s.recv(1024)
    iv = s.recv(1024)
    s.close()

    return K, iv


# Discuta cu nodurile A si B pentru a le oferi cheile criptate pentru
# criptarea/decriptare mesajului (in functie de modul de operare dorit)


def A_B_discussion():
    s = socket.socket()
    host = socket.gethostname()
    port = 112

    s.bind((host, port))

    s.listen()
    if True:
        c, adr = s.accept()
        print("Got conection with node A")
        mesaj = c.recv(1024)
        if mesaj == b"ecb":
            print("\nTrimitem cheia criptata k1 lui A:  ", ciphertext_k1)
            c.send(ciphertext_k1)
        else:
            print("\nTrimitem cheia criptata k2 lui A:  ", ciphertext_k2)
            c.send(ciphertext_k2)
        c.close()

    if True:
        c, adr = s.accept()
        print("Got conection with node B")
        mesaj = c.recv(1024)
        if mesaj == b"ecb":
            print("\nTrimitem cheia criptata k1 lui B:  ", ciphertext_k1)
            c.send(ciphertext_k1)
        else:
            print("\nTrimitem cheia criptata k1 lui B:  ", ciphertext_k1)
            c.send(ciphertext_k2)
        c.close()

    s.close()


# Realizeaza cheile k1(modul ECB) si k2(modul CFB) random


def random_key():
    k1 = str.encode(
        ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
    k2 = str.encode(
        ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
    return k1, k2


# Cripteaza cheile k1 si k2 pentru a le trimite mai departe nodurilor A si B
# (atunci cand sunt cerute)


def encrypt_k1(k):
    key_encrypt = AES.new(K, AES.MODE_ECB)
    ciphertext = key_encrypt.encrypt(k)
    return ciphertext


def encrypt_k2(k):
    iv_encrypt = AES.new(K, AES.MODE_ECB)
    cipher = iv_encrypt.encrypt(iv)
    ciphertext = bytes([_a ^ _b for _a, _b in zip(cipher, k)])
    return ciphertext


key_length = 128

K, iv = generator_discussion()
print("Am preluat valorile generate:  ", K, iv)

k1, k2 = random_key()
print("\nGeneram cheile k1 si k2:  ", k1 , k2)

ciphertext_k1 = encrypt_k1(k1)
ciphertext_k2 = encrypt_k2(k2)

A_B_discussion()
