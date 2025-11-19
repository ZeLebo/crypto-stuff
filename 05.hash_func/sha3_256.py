from copy import deepcopy
from functools import reduce


# noinspection PyMethodMayBeStatic,PyUnresolvedReferences
class Sha3:
    def __init__(self, length: int):
        self.type = length
        self.configs = {
            224: {
                "r": 1152,
                "c": 448
            },
            256: {
                "r": 1088,
                "c": 512
            },
            384: {
                "r": 832,
                "c": 768
            },
            512: {
                "r": 576,
                "c": 1024
            }
        }

    # rotate left
    def shift64(self, a: int, n: int) -> int:
        return ((a >> (64 - (n % 64))) + (a << (n % 64))) % (1 << 64)

    # convert 8 bytes to 64 bit int
    def to64(self, num: bytearray) -> int:
        return int.from_bytes(num, byteorder="little")

    # convert 64 bit int to 8 bytes
    def from64(self, num: int) -> bytearray:
        return bytearray(num.to_bytes(8, byteorder="little"))

    # transpose
    def transpose(self, arr: [[]]) -> []:
        out = []
        # make a tuple of all first elements, all second ...
        for tup in zip(*arr):
            out.append(tup)
        return out

    # split the message into chunks
    def split_into_chunks(self, array, chunk_size) -> [[]]:
        size = chunk_size if chunk_size > 0 else 1
        out = []
        for i in range(0, len(array), size):
            out.append(array[i:i + size])
        return out

    # convert 3d array to 1d array
    def two_to_one_dimension(self, arr) -> []:
        out = []
        for sublist in arr:
            for elem in sublist:
                out.append(elem)
        return out

    # convert 2d array to 1d
    def one_to_three_dimension(self, arr) -> [[]]:
        out = []
        for i in range(5):
            out.append([])
            for j in range(5):
                out[i].append(self.to64(arr[8 * (5 * j + i):8 * (5 * j + i) + 8]))
        return out

    # convert 1d array to 3d array
    def three_to_one_dimension(self, arr) -> bytearray:
        flatten = self.two_to_one_dimension(self.transpose(arr))
        out = []
        for elem in flatten:
            out.append(self.from64(elem))
        out = bytearray(self.two_to_one_dimension(out))
        return out

    # permute the chunk (in 3d array)
    def chunk_permutation(self, A):
        R = 1
        for rnd in range(24):
            C = self.making_C(A)
            D = self.making_D(C)
            A = self.xor_arr(A, D)

            i, j = 1, 0
            current = A[1][0]
            for t in range(24):
                i, j = j, (2 * i + 3 * j) % 5
                current, A[i][j] = A[i][j], self.shift64(current, (t + 1) * (t + 2) // 2)

            B = deepcopy(A)
            for (i, j) in self._cartesian_product(range(5), range(5)):
                A[i][j] = B[i][j] ^ ((~B[(i + 1) % 5][j]) & B[(i + 2) % 5][j])

            A, R = self.rc(A, R)
        return A

    def permutation(self, arr) -> bytearray:
        out = self.one_to_three_dimension(arr)
        out = self.chunk_permutation(out)
        return self.three_to_one_dimension(out)
    # absorb the data

    def absorb(self, bytes_r, chunked_data, message):
        for block, index in zip(chunked_data, range(len(chunked_data))):
            block_len = len(block)
            for i in range(block_len):
                message[i] ^= block[i]
            if block_len == bytes_r:
                message = self.permutation(message)
        return message

    def padding(self, bytes_r, chunked_data, l_const, state):
        block_size = len(chunked_data[-1]) if len(chunked_data) != 0 else 0
        state[block_size % bytes_r] ^= l_const
        state[bytes_r - 1] = state[bytes_r - 1] ^ 0x80
        return self.permutation(state)

    def _cartesian_product(self, *arrays):
        import itertools
        return list(itertools.product(*arrays))

    def making_C(self, A):
        C = []
        for row in A:
            C.append(reduce(lambda a, b: a ^ b, row))
        return C

    def making_D(self, C):
        D = []
        for i in range(5):
            D.append(C[i - 1] ^ self.shift64(C[(i + 1) % 5], 1))
        return D

    def xor_arr(self, A, D):
        tmp = []
        for i in range(5):
            tmp.append([])
            for j in range(5):
                tmp[i].append(A[i][j] ^ D[i])
        return tmp
    # rc func

    def rc(self, A, R):
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256
            if R & 2:
                A[0][0] = A[0][0] ^ (1 << ((1 << j) - 1))
        return A, R

    def hash(self, data) -> bytearray:
        l_const = 6
        # size 25 * 2 ** l
        result = bytearray(1600)

        bytes_r = self.configs[self.type]["r"] // 8
        chunked_data = self.split_into_chunks(data, bytes_r)
        # absorbing the data
        '''
        Each block is padded with zeros to a string of length r bits.
        The last block is padded with a single 1 bit, 
        followed by as many 0 bits as necessary to fill the last block.
        '''
        result = self.absorb(bytes_r, chunked_data, result)
        result = self.padding(bytes_r, chunked_data, l_const, result)
        # squeezing the data
        '''
        The output is extracted in blocks of length c bits.
        '''
        return result[:self.type // 8]