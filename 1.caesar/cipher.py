def caesar_cipher(text, key, mode='encrypt'):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            base = ord('a')
            offset = (ord(char) - base + key) % 26 if mode == 'encrypt' else (ord(char) - base - key) % 26
            result.append(chr(base + offset))
        elif 'A' <= char <= 'Z':
            base = ord('A')
            offset = (ord(char) - base + key) % 26 if mode == 'encrypt' else (ord(char) - base - key) % 26
            result.append(chr(base + offset))
        else:
            result.append(char)
    return ''.join(result)

if __name__ == "__main__":
    mode = input("Введите 'encrypt' для зашифровки или 'decrypt' для расшифровки: ")
    key = 3
    if (mode == 'encrypt'):
        text = input("Введите текст для зашифровки: ")
        encrypted_text = caesar_cipher(text, key, mode='encrypt')
        print("Зашифрованный текст:", encrypted_text)
    elif (mode == 'decrypt'):
        encrypted_text = input("Введите текст для расшифровки: ")
        decrypted_text = caesar_cipher(encrypted_text, key, mode='decrypt')
        print("Расшифрованный текст:", decrypted_text)
