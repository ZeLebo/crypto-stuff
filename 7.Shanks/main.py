from collections import defaultdict
def discrete_log_shanks_verbose(g, h, p, verbose=True):
    """
    Метод Шэнкса с подробным выводом и подсчетом умножений.
    Решает задачу g^x ≡ h (mod p).
    """
    count_multiplications = 0

    m = 1
    while m * m < p:
        m += 1

    if verbose: print(f"Выбрано m = {m}")

    baby_steps = defaultdict(int)
    current = 1
    if verbose: print("\nbaby step phase:")
    for j in range(m):
        baby_steps[current] = j
        if verbose: print(f"j = {j}: g^{j} ≡ {current} (mod {p})")
        current = (current * g) % p
        count_multiplications += 1

    # g^(-m) mod p
    inverse_g_m = pow(g, m * (p - 2), p)
    if verbose: print(f"\ninverse phase: g^(-m) ≡ {inverse_g_m} (mod {p})")
    count_multiplications += m  # pow() выполняет O(log(m)) умножений

    giant = h
    if verbose: print("\ngiant step phase:")
    for i in range(m):
        if verbose: print(f"i = {i}: h * (g^(-m))^i ≡ {giant} (mod {p})")
        if giant in baby_steps:
            j = baby_steps[giant]
            if verbose: print(f"found j: j = {j}, i = {i}")
            return i * m + j, count_multiplications
        giant = (giant * inverse_g_m) % p
        count_multiplications += 1

    return None, count_multiplications


def brute_force_discrete_log(g, h, p):
    """
    Полный перебор для дискретного логарифмирования
    """
    count_multiplications = 0
    current = 1
    for x in range(p):
        if current == h:
            return x, count_multiplications
        current = (current * g) % p
        count_multiplications += 1
    return None, count_multiplications

g = 5
h = 25
p = 1000

result, multiplications = discrete_log_shanks_verbose(g, h, p, verbose=False)
print(f"\nШенкс: g^x ≡ h (mod p) => x = {result}, Умножений: {multiplications}")

result_brute, multiplications_brute = brute_force_discrete_log(g, h, p)
print(f"Полный перебор: g^x ≡ h (mod p) => x = {result_brute}, Умножений: {multiplications_brute}")