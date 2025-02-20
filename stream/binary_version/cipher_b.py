def xor_files(input_file, key_file, output_file):
    with open(input_file, 'rb') as plaintext, open(key_file, 'rb') as key, open(output_file, 'wb') as ciphertext:
        while True:
            plaintext_byte = plaintext.read(1)
            key_byte = key.read(1)
            
            if not plaintext_byte or not key_byte:
                break
            
            result_byte = bytes([plaintext_byte[0] ^ key_byte[0]])
            ciphertext.write(result_byte)

if __name__=="__main__":
    import os
    if not os.path.exists('key.bin'):
        import generator_b as generator
        generator.generate_random_key_file('key.bin', 1024)
    if not os.path.exists('plaintext.txt'):
        with open('plaintext.txt', 'w') as f:
            f.write('Hello, World!')
    xor_files('plaintext.txt', 'key.bin', 'ciphertext.bin')
    xor_files('ciphertext.bin', 'key.bin', 'decrypted.txt')