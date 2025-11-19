"""Генерирует keystream для RC4."""
def rc4_keystream(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]

"""Шифрует/расшифровывает текстовый файл с помощью RC4."""
def rc4_encrypt_decrypt_text(input_file, key, output_file):
    keystream = rc4_keystream(key)
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        while (char := infile.read(1)):
            char_code = ord(char)
            
            keystream_value = next(keystream)
            encrypted_code = char_code ^ keystream_value
            
            encrypted_char = chr(encrypted_code)
            outfile.write(encrypted_char)

if __name__ == "__main__":
    key = "secretkey"
    import os
    if not os.path.exists('files/key.txt'):
        import generator
        generator.generate_random_text_key_file('files/key.txt', 1024)
    if not os.path.exists('files/plaintext.txt'):
        with open('files/plaintext.txt', 'w') as f:
            f.write('Hello, World!')
    with open('files/key.txt') as f:
        key = f.read()
    rc4_encrypt_decrypt_text('files/plaintext.txt', key, 'files/rc_encrypted.txt')
    rc4_encrypt_decrypt_text('files/rc_encrypted.txt', key, 'files/decrypted.txt')
