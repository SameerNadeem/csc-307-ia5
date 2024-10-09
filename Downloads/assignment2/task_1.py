from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


def pad_pkcs7(data, block_size):
    padding_size = block_size - len(data) % block_size # no of padding bytes needed
    padding = bytes([padding_size]) * padding_size # creation of padding bytes
    return data + padding 

#generate a random AES key 
def generate_key_and_iv():
    key = get_random_bytes(16) 
    iv = get_random_bytes(16) # random 16-byte IV for CBC mode
    return key, iv 

#encrypt data using AES in ECB mode
def encrypt_ecb(data, key):
    cipher = AES.new(key, AES.MODE_ECB) # Initialize AES cipher in ECB
    ciphertext = b"" # Empty byte string to store encrypted data

    for i in range(0, len(data), 16):
        block = data[i:i+16]
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block

    return ciphertext

def encrypt_cbc(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = b""

    for i in range(0, len(data), 16):
        block = data[i:i+16]
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block

    return ciphertext

header_size = 54
text_file = "cp-logo.bmp"
with open(text_file, "rb") as file:
    header = file.read(header_size)
    plaintext = file.read()

key, iv = generate_key_and_iv()

ecb_ciphertext = encrypt_ecb(pad_pkcs7(plaintext, 16), key)

cbc_ciphertext = encrypt_cbc(pad_pkcs7(plaintext, 16), key, iv)

with open("ecb_ciphertext.bmp", "wb") as file:
    file.write(header + ecb_ciphertext)

with open("cbc_ciphertext.bmp", "wb") as file:
    file.write(header + cbc_ciphertext)
