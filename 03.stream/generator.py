import random
import string

def generate_random_text_key_file(file_path, size, charset=string.ascii_letters):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(random.choice(charset) for _ in range(size)))
        
if __name__ == "__main__":
    generate_random_text_key_file('files/key.txt', 1024)
