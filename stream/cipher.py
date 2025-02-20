"""Выполняет XOR двух текстовых файлов и записывает результат в третий файл."""
def xor_text_files(input_file, key_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as plaintext, \
         open(key_file, 'r', encoding='utf-8') as key, \
         open(output_file, 'w', encoding='utf-8') as ciphertext:
        
        while True:
            plaintext_char = plaintext.read(1)
            key_char = key.read(1)
            
            if not plaintext_char or not key_char:
                break
            
            plaintext_code = ord(plaintext_char)
            key_code = ord(key_char)
            
            result_code = plaintext_code ^ key_code
            
            # back to symbol
            result_char = chr(result_code)
            ciphertext.write(result_char)


if __name__=="__main__":
    import os
    if not os.path.exists('files/key.txt'):
        import generator
        generator.generate_random_text_key_file('files/key.txt', 1024)
    if not os.path.exists('files/plaintext.txt'):
        with open('files/plaintext.txt', 'w') as f:
            f.write('Hello, World!')
    xor_text_files('files/plaintext.txt', 'files/key.txt', 'files/ciphertext.txt')
    xor_text_files('files/ciphertext.txt', 'files/key.txt', 'files/decrypted.txt')
