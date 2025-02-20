import requests

class CaesarCipher:
    def __init__(self):
        self.dictionary = None

    def caesar_cipher(self, text, key, mode='encrypt'):
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
                result.append(char)  # Не изменяем неалфавитные символы
        return ''.join(result)

    def load_dictionary(self):
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
        response = requests.get(url)
        if response.status_code == 200:
            self.dictionary = set(word.strip().lower() for word in response.text.splitlines())
        else:
            raise Exception("Cannot load the dictionary")

    def is_meaningful(self, text):
        if not self.dictionary:
            raise Exception("Dictionary is not loaded. Call load_dictionary() first.")
        
        words = text.lower().split()
        meaningful_word_count = sum(1 for word in words if word in self.dictionary)
        return len(words) > 0 and meaningful_word_count / len(words) > 0.5

    def find_key_with_dictionary(self, cipher_text):
        if not self.dictionary:
            raise Exception("Dictionary is not loaded. Call load_dictionary() first.")
        
        for key in range(26):
            decrypted_text = self.caesar_cipher(cipher_text, key, mode='decrypt')
            if self.is_meaningful(decrypted_text):
                return key, decrypted_text
        return None, None


# Пример использования
if __name__ == "__main__":
    cipher = CaesarCipher()

    # Загрузка словаря
    try:
        cipher.load_dictionary()
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Зашифрованный текст
    cipher_text = "Khoor vxfk d qlfh gdb wrgdb"

    # Поиск ключа
    key, decrypted_text = cipher.find_key_with_dictionary(cipher_text)
    if key is not None:
        print(f"Найден ключ: {key}, Расшифрованный текст: {decrypted_text}")
    else:
        print("Ключ не найден")