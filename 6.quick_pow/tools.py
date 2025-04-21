"""
Раскладываем exponent на двоичный вид
Последовательно умножаем на 2 основание
Получаем log2(exponent) шагов, а не exponent
"""
def fast_pow(base, exponent, mod=None, verbose=True):
    result = 1
    current = base
    square_steps = 0
    mult_steps = 0

    while exponent > 0:
        if verbose:
            print(f"exp: {exponent}, current base: {current}, result: {result}")

        if exponent % 2:
            result = result * current
            mult_steps += 1

            if mod: result %= mod
            if verbose: print(f"  multiplied -> result: {result}")

        current = current * current
        square_steps += 1

        if mod: current %= mod
        exponent //= 2

    print(f"Final result: {result}, square steps: {square_steps}, mult steps: {mult_steps}") if verbose else None
    return result, square_steps + mult_steps

def naive_pow(a, b, m=None):
    result = 1
    for _ in range(b):
        result *= a
        if m:
            result %= m
    return result