import random
import string
import socket

key_length = 128

# Generam random cheia K si vectorul de initializare vi

K = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
iv = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))

# Oferim cheia si vectorul de initializare generate celor 3 noduri (A, B, MC) prin retea

s = socket.socket()
host = socket.gethostname()
port = 111

s.bind((host, port))

s.listen()
if True:
    c, adr = s.accept()
    print("Got conection from node MC")
    c.send(K)
    c.send(iv)
    c.close()

if True:
    c, adr = s.accept()
    print("Got conection from node A")
    c.send(K)
    c.send(iv)
    c.close()

if True:
    c, adr = s.accept()
    print("Got conection from node B")
    c.send(K)
    c.send(iv)
    c.close()

s.close()
