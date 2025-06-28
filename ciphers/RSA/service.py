from rsa_implementation import RSA


class Service:
    def __init__(self):
        self.rsa = RSA()

    def generate_keys(self, key_size):
        return self.rsa.generate_keys(key_size)

    def encrypt(self, message, public_key):
        return self.rsa.encrypt(message, public_key)

    def decrypt(self, message, private_key):
        tmp = self.rsa.decrypt(message, private_key)
        return RSA.int2bytes(tmp).decode()

    def sign(self, message, private_key):
        return self.rsa.sign(message, private_key)

    def verify(self, message, signature, public_key):
        res = self.rsa.verify(message, signature, public_key)
        if res:
            return "Signature is valid"
        else:
            raise Exception("Signature is not valid")

    def load_keys(self):
        return self.rsa.load_keys()
