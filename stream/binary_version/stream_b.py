from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def rc4_encrypt_decrypt(input_file, key, output_file):
    backend = default_backend()
    cipher = Cipher(algorithms.ARC4(key), mode=None, backend=backend)
    encryptor = cipher.encryptor()
    
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while chunk := infile.read(1024):
            outfile.write(encryptor.update(chunk))

if __name__=="__main__":
    rc4_encrypt_decrypt('files/plaintext.txt', b'secretkey', 'files/encrypted_rc4.bin')
    rc4_encrypt_decrypt('files/encrypted_rc4.bin', b'secretkey', 'files/decrypted_rc4.txt')