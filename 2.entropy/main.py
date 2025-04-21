from collections import Counter
import math
import random
import os

# Функция для подсчета частот символов в текстовом файле
def calculate_frequencies(file_path):
    frequencies = Counter()
    total_characters = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        while (char := file.read(1)):
            if char:  # Проверяем, что прочитан символ
                frequencies[char] += 1
                total_characters += 1
    
    probabilities = {char: freq / total_characters for char, freq in frequencies.items()}
    return probabilities, total_characters

# Функция для вычисления энтропии
def calculate_entropy(probabilities):
    entropy = 0.0
    for prob in probabilities.values():
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

# Функция для анализа файла
def analyze_file(file_path):
    probabilities, total_characters = calculate_frequencies(file_path)
    entropy = calculate_entropy(probabilities)
    
    print(f"Анализ файла: {file_path}")
    print(f"Общее количество символов: {total_characters}")
    print("Частоты символов:")
    for char, prob in probabilities.items():
        print(f"Символ: {repr(char)}, Частота: {prob:.6f}")
    print(f"Энтропия: {entropy:.6f}\n")

# Функция для генерации тестовых файлов в текстовом формате
def generate_test_files():
    # Файл с одинаковыми символами
    with open('same_chars.txt', 'w', encoding='utf-8') as file:
        file.write('A' * 1000)
    
    # Файл со случайными символами '0' и '1'
    with open('random_01.txt', 'w', encoding='utf-8') as file:
        file.write(''.join(random.choice(['0', '1']) for _ in range(1000)))
    
    # Файл со случайными английскими буквами
    with open('random_letters.txt', 'w', encoding='utf-8') as file:
        file.write(''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000)))

if __name__ == "__main__":
    generate_test_files()
    files_to_analyze = ['same_chars.txt', 'random_01.txt', 'random_letters.txt']
    
    for file in files_to_analyze:
        analyze_file(file)

    # delete files after analysis
    for file in files_to_analyze:
        try:
            os.remove(file)
        except OSError:
            pass