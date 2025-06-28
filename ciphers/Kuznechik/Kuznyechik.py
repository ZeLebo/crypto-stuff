"""
КУЗнецов, НЕчаев и Компания
"""
from typing import List

from Consts import _KEY_SIZE as _KEY_SIZE
from Consts import TEST_KEY as TEST_KEY
from Consts import _BLOCK_SIZE_KUZNYECHIK as _BLOCK_SIZE_KUZNYECHIK
from Consts import _GF as GALUA_FIELDS
from Consts import _S_BOX_KUZNYECHIK as _S_BOX_KUZNYECHIK
from Consts import _S_BOX_REVERSE_KUZNYECHIK as _S_BOX_REVERSE_KUZNYECHIK


class Kuznyechik:
    def __init__(self, key=None):
        if key is None:
            key = TEST_KEY
        self.consts: List[bytearray] = []
        self.keys = []
        self.get_constant()
        key_1 = key[:_KEY_SIZE // 2]
        key_2 = key[_KEY_SIZE // 2:]
        self.keys.append(key_1)
        self.keys.append(key_2)
        for i in range(4):
            for j in range(8):
                internal = self.add_xor(key_1, self.consts[i * 8 + j])
                internal = Kuznyechik.non_linear_s(internal)
                internal = Kuznyechik.linear_l(internal)
                key_1, key_2 = [self.add_xor(internal, key_2), key_1]
            self.keys.append(key_1)
            self.keys.append(key_2)

    @staticmethod
    def add_xor(a: bytearray, b: bytearray) -> bytearray:
        result_len = min(len(a), len(b))
        result = bytearray(result_len)
        for i in range(result_len):
            result[i] = a[i] ^ b[i]
        return result

    @staticmethod
    def non_linear_s(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNYECHIK)
        for i in range(_BLOCK_SIZE_KUZNYECHIK):
            result[i] = _S_BOX_KUZNYECHIK[data[i]]
        return result

    @staticmethod
    def non_linear_s_reverse(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNYECHIK)
        for i in range(_BLOCK_SIZE_KUZNYECHIK):
            result[i] = _S_BOX_REVERSE_KUZNYECHIK[data[i]]
        return result

    @staticmethod
    def _cipher_r(data: bytearray) -> bytearray:
        a_0 = 0
        result = bytearray(_BLOCK_SIZE_KUZNYECHIK)
        for i in range(_BLOCK_SIZE_KUZNYECHIK):
            result[i] = data[i - 1]
            a_0 = a_0 ^ GALUA_FIELDS[i][result[i]]
        result[0] = a_0
        return result

    @staticmethod
    def _cipher_r_reverse(data: bytearray) -> bytearray:
        a_15 = 0
        result = bytearray(_BLOCK_SIZE_KUZNYECHIK)
        for i in range(_BLOCK_SIZE_KUZNYECHIK - 1, -1, -1):
            result[i - 1] = data[i]
            a_15 = a_15 ^ GALUA_FIELDS[i][data[i]]
        result[15] = a_15
        return result

    @staticmethod
    def linear_l(data: bytearray) -> bytearray:
        result = data
        for _ in range(16):
            result = Kuznyechik._cipher_r(result)
        return result

    @staticmethod
    def linear_l_reverse(data: bytearray) -> bytearray:
        result = data
        for _ in range(16):
            result = Kuznyechik._cipher_r_reverse(result)
        return result

    def get_constant(self) -> None:
        for i in range(1, 33):
            internal = bytearray(_BLOCK_SIZE_KUZNYECHIK)
            internal[15] = i
            self.consts.append(Kuznyechik.linear_l(internal))

    def decrypt(self, block: bytearray) -> bytearray:
        block = bytearray(block)
        block = self.add_xor(self.keys[9], block)
        for i in range(8, -1, -1):
            block = Kuznyechik.linear_l_reverse(block)
            block = Kuznyechik.non_linear_s_reverse(block)
            block = self.add_xor(self.keys[i], block)
        return block

    def encrypt(self, block: bytearray) -> bytearray:
        block = bytearray(block)
        for i in range(9):
            block = self.add_xor(self.keys[i], block)
            block = Kuznyechik.non_linear_s(block)
            block = Kuznyechik.linear_l(block)
        block = self.add_xor(self.keys[9], block)
        return block

    @staticmethod
    def _prepare_data(data: str) -> list[int | bytearray]:
        # convert to byte array
        data = bytearray(data.encode())
        # add padding
        for _ in range(16 - len(data) % 16):
            data += b'\x00'
        # split into chunks
        data = [data[i:i + 16] for i in range(0, len(data), 16)]
        return data

    @staticmethod
    def _convert_to_string(data: list[int | bytearray]) -> str:
        # merge all chunks
        data = b"".join(data)
        # remove padding
        data = data.rstrip(b'\x00')
        return data.decode()

    def hash_to_string(self, data: str) -> str:
        data = self._prepare_data(data)
        data = [self.encrypt(block) for block in data]
        data = ''.join([hex(i)[2:] for i in data[0]])
        return data

    def hash(self, data: str) -> list[int | bytearray]:
        data = self._prepare_data(data)
        data = [self.encrypt(block) for block in data]
        return data

    def from_hash(self, data: list[int | bytearray]) -> str:
        data = [self.decrypt(block) for block in data]
        data = self._convert_to_string(data)
        return data

    def running_hash(self, data: str) -> str:
        data = self._prepare_data(data)
        data = [self.encrypt(block) for block in data]
        data = [self.decrypt(block) for block in data]
        data = self._convert_to_string(data)
        return data


def main():
    kuz = Kuznyechik()
    print("Rand0m testing")
    string = 'Hello, world!' * 1000
    hashed_string = kuz.hash_to_string(string)
    # print hash as string
    print(hashed_string)
    hashed = kuz.hash(string)
    string_from_hash = kuz.from_hash(hashed)
    print(string_from_hash)
    print(kuz.running_hash(string))

    from pygost import gost3412 as gost
    ENCRYPT_TEST_STRING = bytearray([
        0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x00, 0xff, 0xee, 0xdd, 0xcc, 0xbb, 0xaa, 0x99, 0x88,
    ])

    DECRYPT_TEST_STRING = bytearray([
        0x7f, 0x67, 0x9d, 0x90, 0xbe, 0xbc, 0x24, 0x30, 0x5a, 0x46, 0x8d, 0x42, 0xb9, 0xd4, 0xed, 0xcd,
    ])
    print("Checking encryption")
    myver = ''.join([hex(i)[2:] for i in kuz.encrypt(ENCRYPT_TEST_STRING)])
    orig = ''.join([hex(i)[2:] for i in gost.GOST3412Kuznechik(TEST_KEY).encrypt(ENCRYPT_TEST_STRING)])
    print(myver)
    if myver == orig:
        print("The hashes are the same")
    else:
        print("The hashes are different")

    print("Checking decryption")
    myver = ''.join([hex(i)[2:] for i in kuz.decrypt(DECRYPT_TEST_STRING)])
    orig = ''.join([hex(i)[2:] for i in gost.GOST3412Kuznechik(TEST_KEY).decrypt(DECRYPT_TEST_STRING)])
    print(myver)
    if myver == orig:
        print("The hashes are the same")
    else:
        print("The hashes are different")


if __name__ == '__main__':
    main()
