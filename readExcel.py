import pandas as pdb

import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

import os

#secret key can be anything
secret_key = b'1234567890123456'
df = pdb.read_excel('SalesLead.xlsx')
key = os.urandom(32);

#method to encrypt the data
def encrypt(key, plaintext, associated_data):
    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (iv, ciphertext, encryptor.tag)

#method to decrypt the data
def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()

#for testing 
for i in df['Contact']:
    iv, ciphertext, tag = encrypt(
        key,
        str(i).encode(),
        b"authenticated but not encrypted payload"
    )
    print("---------------------------------------------")
    print("Cipher Text: ")
    print(ciphertext)
    print("Decipher Text: ")
    print(decrypt(
        key,
        b"authenticated but not encrypted payload",
        iv,
        ciphertext,
        tag
    ))
print("---------------------------------------------")
