def find_caesar_key(plain_text, cipher_text):
    for p_char, c_char in zip(plain_text, cipher_text):
        if 'a' <= p_char <= 'z' and 'a' <= c_char <= 'z':
            return (ord(c_char) - ord(p_char)) % 26
        elif 'A' <= p_char <= 'Z' and 'A' <= c_char <= 'Z':
            return (ord(c_char) - ord(p_char)) % 26
    return None

if __name__ == "__main__":
    plain_text = "hello"
    cipher_text = "khoor"
    key = find_caesar_key(plain_text, cipher_text)
    print("Ключ шифрования:", key)