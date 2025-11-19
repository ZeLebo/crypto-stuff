from collections import Counter
import math
import random

def calculate_frequencies(file_path):
    frequencies = Counter()
    total_characters = 0
    
    with open(file_path, 'rb') as file:
        while (byte := file.read(1)):
            frequencies[byte] += 1
            total_characters += 1
    
    probabilities = {char: freq / total_characters for char, freq in frequencies.items()}
    return probabilities, total_characters

def calculate_entropy(probabilities):
    entropy = 0.0
    for prob in probabilities.values():
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def analyze_file(file_path):
    probabilities, total_characters = calculate_frequencies(file_path)
    entropy = calculate_entropy(probabilities)
    
    print(f"Анализ файла: {file_path}")
    print(f"Общее количество символов: {total_characters}")
    print("Частоты символов:")
    for char, prob in probabilities.items():
        print(f"Символ: {char.decode('latin1', errors='replace')} (код: {ord(char)}), Частота: {prob:.6f}")
    print(f"Энтропия: {entropy:.6f}\n")

def generate_test_files():
    with open('same_chars.txt', 'wb') as file:
        file.write(b'A' * 1000)
    
    with open('random_01.txt', 'wb') as file:
        file.write(bytes(random.choice([0, 1]) for _ in range(1000)))
    
    with open('random_all.txt', 'wb') as file:
        file.write(bytes(random.randint(0, 255) for _ in range(1000)))

if __name__ == "__main__":
    generate_test_files()
    files_to_analyze = ['same_chars.txt', 'random_01.txt', 'random_all.txt']
    
    for file in files_to_analyze:
        analyze_file(file)

    import os
    for file in files_to_analyze:
        try:
            os.remove(file)
        except OSError:
            pass