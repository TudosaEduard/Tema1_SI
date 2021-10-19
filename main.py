import random
import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Node MC implementation

key_length = 128

# Generate keys randomly for encrypting and decrypting keys

K = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
k1 = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))
k2 = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))

# print("Keys are : ", K, k1, k2)

k1_cipher_encrypt = AES.new(K, AES.MODE_ECB)
k1_ciphertext = k1_cipher_encrypt.encrypt(k1)

# print(k1_ciphertext)

k1_cipher_decrypt = AES.new(K, AES.MODE_ECB)
k1_plaintext = k1_cipher_decrypt.decrypt(k1_ciphertext)

# print(k1.decode(), k1_plaintext.decode())

iv = str.encode(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=key_length // 8)))

iv_cipher_encrypt = AES.new(K, AES.MODE_ECB)
iv_ciphertext = iv_cipher_encrypt.encrypt(iv)

k2_ciphertext = bytes([_a ^ _b for _a, _b in zip(iv_ciphertext, k2)])

# print(k2_ciphertext)

iv_cipher_decrypt = AES.new(K, AES.MODE_ECB)
iv_plaintext = iv_cipher_decrypt.encrypt(iv)

k2_plaintext = bytes([_a ^ _b for _a, _b in zip(iv_plaintext, k2_ciphertext)])

# print(k2, k2_plaintext)

readfile1 = open('mesaj.txt', 'r')
# print(readfile.read())

text_encrypt = str.encode("")
while readfile1:
    block_cipher_encrypt = AES.new(k1, AES.MODE_ECB)
    block = str.encode(readfile1.read(key_length // 8))
    block_ciphertext = block_cipher_encrypt.encrypt(pad(block, key_length // 8))

    # print(block_ciphertext)
    text_encrypt = text_encrypt + block_ciphertext

    if block.decode() == "":
        break
readfile1.close()
# print(text_encrypt)

index = 0
text = b""

while index <= len(text_encrypt):
    block_cipher_decrypt = AES.new(k1, AES.MODE_ECB)
    block_plaintext = block_cipher_decrypt.decrypt(text_encrypt[index:(index + 16)])

    print(block_plaintext)

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
# print(text.decode())


readfile2 = open('mesaj.txt', 'r')

text_encrypt = str.encode("")

key_vector = iv
while readfile2:
    key_encrypt = AES.new(k2, AES.MODE_ECB)
    key_encrypt_cfb = key_encrypt.encrypt(pad(key_vector, key_length // 8))
    block = str.encode(readfile2.read(key_length // 8))
    block_ciphertext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, block)])

    # print(block_ciphertext)
    text_encrypt = text_encrypt + block_ciphertext
    key_vector = block_ciphertext

    if block.decode() == "":
        break
readfile2.close()

# print(text_encrypt)

index = 0
text = b""

while index <= len(text_encrypt):
    key_encrypt = AES.new(k2, AES.MODE_ECB)
    key_encrypt_cfb = key_encrypt.encrypt(pad(iv, key_length // 8))

    block_plaintext = bytes([_a ^ _b for _a, _b in zip(key_encrypt_cfb, text_encrypt[index:(index + 16)])])
    text = text + block_plaintext
    iv = text_encrypt[index:(index + 16)]

    index = index + 16

# print(text.decode())
