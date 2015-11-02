# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from StringIO import StringIO
from werkzeug.datastructures import FileStorage


def generate_secret_key(key_size=32):
    # Genera una clave aleatoria.
    secret_key = Random.get_random_bytes(key_size)
    return secret_key


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")


def encrypt_file(raw_file, key):
    plaintext = raw_file.read()
    enc = encrypt(plaintext, key)
    enc_stream = StringIO()
    enc_stream.write(enc)
    enc_stream.seek(0)
    encrypted_file = FileStorage(enc_stream,
                                 raw_file.filename,
                                 raw_file.name,
                                 raw_file.content_type,
                                 raw_file.content_length,
                                 raw_file.headers
                                 )
    return encrypted_file


def decrypt_file(enc_file, key):
    ciphertext = enc_file
    dec = decrypt(ciphertext, key)
    return dec


def encrypt_secret_key(secret_key, rsa_public_key_plain):
    rsa_public_key = RSA.importKey(rsa_public_key_plain)
    encrypted_secret_key = b64encode(rsa_public_key.encrypt(secret_key, 'x')[0])
    return encrypted_secret_key


def decrypt_secret_key(encrypted_secret_key, rsa_private_key_plain):
    rsa_private_key = RSA.importKey(rsa_private_key_plain)
    secret_key = rsa_private_key.decrypt(b64decode(encrypted_secret_key))
    return secret_key
