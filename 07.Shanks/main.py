import math
from collections import defaultdict
from time import perf_counter
"""
m = sqrt(p) + 1
1. Вычисляем a^j mod p для j от 0 до m-1 и сохраняем в словаре (a^j, j)
2. Вычисляем a^(-m) mod p и сохраняем в переменной
3. Проверяем b * (a^(-m))^i mod p для i от 0 до m-1
    3.1 Если совпадает с элементом из словаря, то x = i * m + j
    3.2 Если совпадает, то x = i * m + j
    3.3 Если не совпадает, то продолжаем
4. Если не нашли совпадение, то x не существует
"""
def baby_step_giant_step(a, b, p):
    print("\n--- Метод Шэнкса (Шаг младенца — шаг великана) ---")
    m = math.isqrt(p) + 1  # Автоматический выбор m
    print(f"Выбрано m = {m} (приблизительно √{p})")

    baby_steps = {}
    current = 1
    mul_count = 0

    print("\nЭтап 1: вычисление шагов младенца:")
    for j in range(m):
        baby_steps[current] = j
        print(f"  a^{j} ≡ {current} mod {p}")
        current = (current * a) % p
        mul_count += 1

    # Вычисляем a^{-m} mod p
    a_inv_m = pow(a, -m, p)
    print(f"\nВычислено a^(-m) ≡ {a_inv_m} mod {p} (обратный элемент)")

    current = b
    print("\nЭтап 2: гигантские шаги:")
    for i in range(m):
        print(f"  Проверяем b * (a^(-m))^{i} ≡ {current} mod {p}")
        if current in baby_steps:
            x = i * m + baby_steps[current]
            print(f"Найдено совпадение: x = {x}\nВсего умножений: {mul_count + i}")
            return x, mul_count + i
        current = (current * a_inv_m) % p
        mul_count += 1

    print("Решение не найдено")
    return None, mul_count


def brute_force_log(a, b, p):
    print("\n--- Полный перебор ---")
    current = 1
    mul_count = 0

    for x in range(p):
        print(f"  a^{x} ≡ {current} mod {p}")
        if current == b:
            print(f"Найдено: x = {x}")
            print(f"Всего умножений: {mul_count}")
            return x, mul_count
        current = (current * a) % p
        mul_count += 1

    print("Решение не найдено")
    return None, mul_count


def compare_methods(a, b, p):
    print(f"\n========== Решение уравнения {a}^x ≡ {b} mod {p} ==========")
    
    baby_start = perf_counter()
    x1, mul1 = baby_step_giant_step(a, b, p)
    baby_end = perf_counter()
    brute_force_start = perf_counter()
    x2, mul2 = brute_force_log(a, b, p)
    brute_force_end = perf_counter()

    print("\n--- Сравнение ---")
    print(f"Метод Шэнкса: x = {x1}, умножений = {mul1}, время = {baby_end - baby_start:.6f} сек")
    print(f"Полный перебор: x = {x2}, умножений = {mul2}, время = {brute_force_end - brute_force_start:.6f} сек")

compare_methods(a=79, b=122, p=263)