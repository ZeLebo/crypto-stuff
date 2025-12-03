from utils import get_public_params, modular_exponentiation, generate_secret_exponent


class User:
    def __init__(self, name):
        self.name = name
        self.P, self.G = get_public_params()
        self.private_exponent = generate_secret_exponent(self.P)
        self.public_key = self._calculate_public_key()
        self.shared_secret = None

    def _calculate_public_key(self):
        """Y = G^a mod P."""
        return modular_exponentiation(self.G, self.private_exponent, self.P)

    def calculate_shared_secret(self, received_public_key):
        """K = Y_partner^a mod P."""
        if self.shared_secret is None:
            self.shared_secret = modular_exponentiation(
                received_public_key,
                self.private_exponent,
                self.P
            )
        return self.shared_secret

    def get_user_data(self):
        return {
            "Name": self.name,
            "Secret exponent (a)": self.private_exponent,
            "Public key (Y)": self.public_key
        }

    def __str__(self):
        return self.name
