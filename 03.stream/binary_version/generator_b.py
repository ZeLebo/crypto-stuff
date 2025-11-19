import random

def generate_random_key_file(file_path, size):
    with open(file_path, 'wb') as file:
        file.write(bytes(random.getrandbits(8) for _ in range(size)))

if __name__ == "__main__":
    generate_random_key_file('key.bin', 1024)