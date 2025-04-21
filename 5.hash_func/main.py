from sha3_256 import Sha3
"""
1. Начинаем с начального значения (seed).
2. Каждый новый выход — это sha3_256 от предыдущего состояния.
3. Из выходного хеша берём нужное количество бит/байт для числа.
"""
class SHA3PRNG:
    def __init__(self, seed: bytes, output_bits: int = 256):
        self.sha3 = Sha3(output_bits)
        self.state = seed

    def next_bytes(self, n: int = 32) -> bytes:
        """
        Генерирует n байт случайных данных.
        """
        out = bytearray()
        while len(out) < n:
            hashed = self.sha3.hash(self.state)
            out.extend(hashed)
            self.state = hashed  # обновляем состояние
        return bytes(out[:n])

    def next_int(self, bits: int = 32) -> int:
        """
        Генерирует случайное целое число заданной битности.
        """
        byte_len = (bits + 7) // 8
        raw_bytes = self.next_bytes(byte_len)
        value = int.from_bytes(raw_bytes, 'big')
        return value >> (byte_len * 8 - bits)

if __name__ == "__main__":
    import os
    seed = os.urandom(32)
    prng = SHA3PRNG(seed)

    print("Псевдослучайные числа:")
    for _ in range(5):
        print(f"int: {prng.next_int()}")
