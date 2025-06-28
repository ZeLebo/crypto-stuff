import unittest
from rsa_implementation import RSA
import rsa.core as core
from hashlib import sha256


class TestRSA(unittest.TestCase):
    def test_encrypt(self):
        test_string = "abracadabra"
        rsa = RSA(keySize=512)
        public, private = rsa.load_keys()

        e, n = public
        d, _ = private
        message = rsa.bytes2int(test_string.encode())
        enc_alg = core.encrypt_int(message, e, n)
        enc_me = rsa.encrypt(message, public)

        self.assertEqual(enc_me, enc_alg)

    def test_decrypt(self):
        test_string = "abracadabra"
        rsa = RSA(keySize=512)
        public, private = rsa.load_keys()

        e, n = public
        d, _ = private
        message = rsa.bytes2int(test_string.encode())
        enc_alg = core.encrypt_int(message, e, n)
        enc_me = rsa.encrypt(message, public)

        dec_me = rsa.decrypt(enc_me, private)
        dec_alc = core.decrypt_int(enc_alg, d, n)
        self.assertEqual(dec_alc, dec_me)
        self.assertEqual(rsa.int2bytes(dec_me).decode(), test_string)

    def test_big_file(self):
        test_string = "abracadabra" * 10000
        chunks, chunk_size = len(test_string), 15
        rsa = RSA(keySize=512)
        for i in [test_string[i:i + chunk_size] for i in range(0, chunks, chunk_size)]:
            public, private = rsa.load_keys()

            signature = rsa.sign(i, private)
            self.assertTrue(rsa.verify(i, signature, public))

    def test_sign(self):
        test_string = "abracadabra"
        rsa = RSA(keySize=512)
        public, private = rsa.load_keys()

        signature = rsa.sign(test_string, private)
        hashed = rsa.bytes2int(sha256(test_string.encode()).digest())
        self.assertEqual(rsa.decrypt(signature, public), hashed)

        # check the signature is correct
        self.assertEqual(signature, core.encrypt_int(hashed, private[0], private[1]))

    def test_verify(self):
        test_string = "abracadabra"
        rsa = RSA(keySize=512)
        public, private = rsa.load_keys()

        signature = rsa.sign(test_string, private)
        self.assertTrue(rsa.verify(test_string, signature, public))
