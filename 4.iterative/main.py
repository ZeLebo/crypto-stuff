import os
import struct

delta = 0x9E3779B9
"""
key: 16 bytes
block: 8 bytes
"""
def tea_encrypt(block, key):
    v0, v1 = struct.unpack("!2I", block) # разбиваем блок на 2 4-х байтных числа
    k0, k1, k2, k3 = struct.unpack("!4I", key) # ключ может быть меньше 16 байт, поэтому дополняем его нулями
    sum_ = 0
    for _ in range(32):
        sum_ = (sum_ + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum_) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum_) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return struct.pack("!2I", v0, v1)

def tea_decrypt(block, key):
    v0, v1 = struct.unpack("!2I", block)
    k0, k1, k2, k3 = struct.unpack("!4I", key.ljust(16, b'\0')[:16])
    sum_ = (delta * 32) & 0xFFFFFFFF
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum_) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum_) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        sum_ = (sum_ - delta) & 0xFFFFFFFF
    return struct.pack("!2I", v0, v1)

def add_padding(data):
    pad_len = 8 - (len(data) % 8)
    return data + b'\x00' * pad_len

def remove_padding(data):
    pad_len = 0
    for byte in reversed(data):
        if byte == 0:
            pad_len += 1
        else:
            break
    return data[:-pad_len] if pad_len > 0 else data

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        plaintext = f_in.read()
        padded_data = add_padding(plaintext) # выравнимаем данные до 8 байт
        for i in range(0, len(padded_data), 8):
            block = padded_data[i:i + 8]
            encrypted_block = tea_encrypt(block, key)
            f_out.write(encrypted_block)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        ciphertext = f_in.read()
        
        block_size = 8
        decrypted_data = b''
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            decrypted_block = tea_decrypt(block, key)
            decrypted_data += decrypted_block

        try:
            unpadded_data = remove_padding(decrypted_data)
        except ValueError as e:
            raise ValueError(f"Cannot remove padding: {e}")

        f_out.write(unpadded_data)

key = os.urandom(16)
encrypt_file("input.txt", "encrypted.bin", key)
decrypt_file("encrypted.bin", "decrypted.txt", key)