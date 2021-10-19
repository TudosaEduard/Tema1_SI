import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

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


# Dupa aflarea modului de operare dorit de nodul A, realizeaza discutia cu nodul
# MC pentru a prelua cheile criptate k1 sau k2 in functie de modul precizat,
# urmand ca apoi sa le decripteze


def MC_discussion(mesaj):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 112  # Reserve a port for your service.

    s.connect((host, port))
    s.send(mesaj)
    k = s.recv(1024)
    s.close()

    return k


def decrypt_key_ecb(k):
    cipher = AES.new(K, AES.MODE_ECB)
    plaintext = cipher.decrypt(k)

    return plaintext


def decrypt_key_cfb(k):
    iv_cipher = AES.new(K, AES.MODE_ECB)
    iv_plaintext = iv_cipher.encrypt(iv)

    plaintext = bytes([_a ^ _b for _a, _b in zip(iv_plaintext, k)])
    return plaintext


# Decripteaza apoi mesajul primit de la nodul A
# in formatul dorit cu ajutorul cheii primite de la nodul MC


def decrypt_text_ecb(enc_mesaj, k):
    index = 0
    text = b""

    while index <= len(enc_mesaj):
        block_cipher_decrypt = AES.new(k, AES.MODE_ECB)
        block_plaintext = block_cipher_decrypt.decrypt(enc_mesaj[index:(index + 16)])

        if block_plaintext.find(b'\x01') != -1 or block_plaintext.find(b'\x02') != -1 or block_plaintext.find(
                b'\x03') != -1:
            text = text + unpad(block_plaintext, key_length // 8)
        else:
            if block_plaintext.find(b'\x04') != -1 or block_plaintext.find(b'\x05') != -1 or block_plaintext.find(
                    b'\x06') != -1:
                text = text + unpad(block_plaintext, key_length // 8)
            else:
                if block_plaintext.find(b'\x07') != -1 or block_plaintext.find(b'\x08') != -1 or block_plaintext.find(
                        b'\x09') != -1:
                    text = text + unpad(block_plaintext, key_length // 8)
                else:
                    if block_plaintext.find(b'\x10') != -1:
                        text = text + unpad(block_plaintext, key_length // 8)
                    else:
                        text = text + block_plaintext
        index = index + 16

    return text.decode()


def decrypt_text_cfb(enc_mesaj, k, iv):
    index = 0
    text = b""

    while index <= len(enc_mesaj):
        key_encrypt = AES.new(k, AES.MODE_ECB)
        key_encrypt_cfb = key_encrypt.encrypt(pad(iv, key_length // 8))

        block_plaintext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, enc_mesaj[index:(index + 16)])])
        text = text + block_plaintext
        iv = enc_mesaj[index:(index + 16)]

        index = index + 16

    return text.decode()


# Se realizeaza discutia cu nodul A in care:
# nodul B afla modul de operare in care va fi criptat textul
# preia cheia pentru decriptarea textului
# confirma nodului A inceperea comunicarii , preia textul si il decripteaza


def A_discussion(iv):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 113  # Reserve a port for your service.

    s.connect((host, port))

    inp = s.recv(1024)
    k = MC_discussion(inp)

    s.send(b"Comunicarea poate incepe (mesaj primit de la B)")
    enc_mesaj = s.recv(1024)
    s.close()
    if inp == b"ecb":
        k = decrypt_key_ecb(k)
        file = open("mesaj_decriptat.txt", "w")
        text = decrypt_text_ecb(enc_mesaj, k)
        file.write(text)
        print(text)
    else:
        k = decrypt_key_cfb(k)
        file = open("mesaj_decriptat.txt", "w")
        text = decrypt_text_cfb(enc_mesaj, k, iv)
        file.write(text)
        print(text)


key_length = 128
K, iv = generator_discussion()
A_discussion(iv)
