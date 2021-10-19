import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

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


# Realizeaza discutia cu nodul MC pentru a prelua cheile criptate k1 sau k2
# in functie de modul precizat, urmand ca apoi sa le decripteze


def MC_discussion(mesaj):
    s = socket.socket()
    host = socket.gethostname()
    port = 112

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


# Cripteaza apoi mesajul in formatul dorit cu ajutorul cheii primite de la nodul MC


def encrypt_text_ecb(k):
    readfile = open('mesaj.txt', 'r')

    text_encrypt = str.encode("")
    while readfile:
        block_cipher = AES.new(k, AES.MODE_ECB)
        block = str.encode(readfile.read(key_length // 8))
        block_ciphertext = block_cipher.encrypt(pad(block, key_length // 8))

        text_encrypt = text_encrypt + block_ciphertext

        if block.decode() == "":
            break
    readfile.close()
    return text_encrypt


def encrypt_text_cfb(k):
    readfile = open('mesaj.txt', 'r')
    text_encrypt = str.encode("")

    key_vector = iv
    while readfile:
        key_encrypt = AES.new(k, AES.MODE_ECB)
        key_encrypt_cfb = key_encrypt.encrypt(pad(key_vector, key_length // 8))
        block = str.encode(readfile.read(key_length // 8))
        block_ciphertext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, block)])

        text_encrypt = text_encrypt + block_ciphertext
        key_vector = block_ciphertext

        if block.decode() == "":
            break
    readfile.close()
    return text_encrypt


# Realizeaza discutia cu nodul B pentru a ii oferi mesajul de decriptat


def B_discussion(inp , enc_mesaj):
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 113  # Reserve a port for your service.

    s.bind((host, port))
    s.listen()
    if True:
        c, adr = s.accept()
        print("Got conection with node B")
        c.send(inp.encode())
        print(c.recv(1024).decode())
        c.send(enc_mesaj)
        c.close()
    s.close()


# In main se preia de la tastatura modul de operare dorit
# se decripteaza cheia luata de la MC
# se cripteaza mesajul si se trimite prin retea nodului B


def main():

    print("Spune ce mod de operare doresti(ecb sau cfb):   ")
    inp = input()
    if inp.lower() == "ecb":
        k = MC_discussion(b"ecb")
        k = decrypt_key_ecb(k)
        B_discussion(inp.lower(), encrypt_text_ecb(k))
    else:
        k = MC_discussion(b"cfb")
        k = decrypt_key_cfb(k)
        B_discussion(inp.lower(), encrypt_text_cfb(k))



key_length = 128
K, iv = generator_discussion()
main()

