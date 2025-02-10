import re
import requests
from cipher import caesar_cipher

def load_dictionary():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    response = requests.get(url)
    if response.status_code == 200:
        dictionary = set(word.strip().lower() for word in response.text.splitlines())
        return dictionary
    else:
        raise Exception("Cannot find the dictionary")

def is_meaningful(text, dictionary):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())  # Извлекаем слова
    meaningful_word_count = sum(1 for word in words if word in dictionary)
    return meaningful_word_count / len(words) > 0.5  # Более 50% слов должны быть осмысленными

def find_key_with_dictionary(cipher_text):
    dictionary = load_dictionary()
    for key in range(26):
        decrypted_text = caesar_cipher(cipher_text, key, mode='decrypt')
        if is_meaningful(decrypted_text, dictionary):
            return key, decrypted_text
    return None, None

if __name__=="__main__":
    cipher_text = "Khoor vxfk d qlfh gdb wrgdb"
    key, decrypted_text = find_key_with_dictionary(cipher_text)
    if key is not None:
        print(f"Найден ключ: {key}, Расшифрованный текст: {decrypted_text}")
    else:
        print("Ключ не найден")