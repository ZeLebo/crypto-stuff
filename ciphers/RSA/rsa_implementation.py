import random
from math import gcd
from hashlib import sha256


class ModularInverseError(Exception):
    pass


class KeysNotGeneratedError(Exception):
    pass


class RSA:
    def __init__(self, keySize=None):
        self.public_key = None
        self.private_key = None
        if keySize is not None:
            if isinstance(keySize, int):
                self.public_key, self.private_key = self.generate_keys(key_size=keySize)
            else:
                raise TypeError("keySize must be an integer")

    def load_keys(self):
        if self.public_key is None or self.private_key is None:
            raise KeysNotGeneratedError()
        return self.public_key, self.private_key

    # Jacobi symbol
    '''
    Jacobi symbol is a function that takes two integers a and n as arguments and returns an integer.
    It is defined for all integers a and odd integers n with a >= 0 and n > 0.
    It is also defined for all integers a and n = 0.
    '''

    @staticmethod
    def jacobi_symbol(a, n) -> int:
        assert n > 0 and n % 2 == 1
        a = a % n
        if a == 0:
            return 0
        t = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                r = n % 8
                if r == 3 or r == 5:
                    t = -t
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                t = -t
            a %= n
        if n == 1:
            return t
        else:
            return 0

    # check prime probability of number (fast probability prime check)
    def is_prime(self, b) -> bool:
        for i in range(100):
            a = random.randint(1, b - 1)
            if (b & 1) == 0:
                return False
            if not (gcd(a, b) == 1 and (self.jacobi_symbol(a, b) + b) % b == pow(a, (b - 1) // 2, b)):
                return False
        return True

    def random_prime(self, a, b) -> int:
        import time
        random.seed(time.time())
        n = random.randint(a, b)
        while not self.is_prime(n):
            n = random.randint(a, b)
        return n

    def generate_primes(self, a, b) -> (int, int):
        return self.random_prime(a, b), self.random_prime(a, b)

    '''
    Extended Euclidean algorithm
    The extended Euclidean algorithm is an extension to the Euclidean algorithm,
    which computes, in addition to the greatest common divisor of integers a and b,
    the coefficients of Bezout's identity, that is, integers x and y such that ax + by = gcd(a, b).
    '''

    def extended_euclidean(self, a, b) -> (int, int, int):
        if a == 0:
            return b, 0, 1
        else:
            # g is the greatest common divisor of a and b
            # x and y are integers such that ax + by = g
            g, y, x = self.extended_euclidean(b % a, a)
            return g, x - (b // a) * y, y

    # Modular multiplicative inverse
    def modular_inverse(self, a, m) -> int:
        g, x, y = self.extended_euclidean(a, m)
        return (x + m) % m if g == 1 else ModularInverseError("modular inverse does not exist")

    """
    generating the key pair, we need to generate two large prime numbers p and q,
    then we calculate n = p * q and phi = (p - 1) * (q - 1)
    then we need to find a number e such that gcd(e, phi) = 1
    then we need to find a number d such that d * e = 1 mod phi
    """
    def generate_keys(self, key_size=1024) -> ((int, int), (int, int)):
        p, q = self.generate_primes((1 << (key_size // 2 - 1)), ((1 << key_size // 2) - 1))

        n = p * q
        phi = (p - 1) * (q - 1)
        d = self.random_prime(max(p, q) + 1, n)
        e = self.modular_inverse(d, phi)
        return (e, n), (d, n)

    @staticmethod
    def bytes2int(b) -> int:
        return int.from_bytes(b, byteorder='big', signed=False)

    @staticmethod
    def int2bytes(number, fill_size=0) -> bytes:
        import math
        bytes_required = max(1, math.ceil(number.bit_length() / 8))

        if fill_size > 0:
            return number.to_bytes(fill_size, "big")

        return number.to_bytes(bytes_required, "big")

    def encrypt_big_file(self, cipher, public_key=None) -> bytes:
        chunk, chunk_size = len(cipher), 256
        if public_key is None:
            if self.public_key is None:
                raise KeysNotGeneratedError()
            public_key = self.public_key
        message = b""
        for i in [cipher[i:i + chunk_size] for i in range(0, chunk, chunk_size)]:
            message += self.int2bytes(self.encrypt(i, public_key))
        return message

    def decrypt_big_file(self, cipher: bytes, private_key) -> bytes:
        chunk, chunk_size = len(cipher), 256
        message = b""
        for i in [cipher[i:i + chunk_size] for i in range(0, chunk, chunk_size)]:
            message += self.int2bytes(self.decrypt(self.bytes2int(i), private_key))
        return message

    def encrypt(self, cipher, public_key=None) -> int:
        if public_key is None:
            if self.public_key is None:
                raise KeysNotGeneratedError()
            public_key = self.public_key
        if isinstance(cipher, str):
            cipher = self.bytes2int(cipher.encode())
        return pow(cipher, public_key[0], public_key[1])

    def decrypt(self, cipher, private_key) -> int:
        # this maybe not work properly, so use ints
        if isinstance(cipher, str):
            cipher = self.bytes2int(cipher.encode())
        return pow(cipher, private_key[0], private_key[1])

    def sign(self, message, private_key) -> int:
        hashed = self.bytes2int(sha256(message.encode()).digest())
        return self.encrypt(hashed, private_key)

    def verify(self, message, signature, public_key) -> bool:
        hashed = self.bytes2int(sha256(message.encode()).digest())
        return self.decrypt(signature, public_key) == hashed
