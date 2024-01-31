from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

def encrypt_aes(data, key):
    # Pad the data using PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create an AES cipher object with a 128-bit key
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the encrypted data
    return ciphertext

def decrypt_aes(ciphertext, key):
    # Create an AES cipher object with a 128-bit key
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

    # Decrypt the data
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the data using PKCS7 unpadding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Return the decrypted data
    return data

# Example usage
key = b'1111111111111111'
plaintext = b'Phoofa'

# Encrypt
ciphertext = encrypt_aes(plaintext, key)
print(f"Ciphertext: {b64encode(ciphertext).decode('utf-8')}")

# Decrypt
decrypted_text = decrypt_aes(ciphertext, key)
print(f"Decrypted Text: {decrypted_text.decode('utf-8')}")