from utils import get_public_params, modular_exponentiation, generate_secret_exponent
from auth import generate_signing_key_pair, sign_message


class User:
    def __init__(self, name):
        self.name = name
        self.P, self.G = get_public_params()

        self.private_exponent = generate_secret_exponent(self.P)
        self.public_key_dh = self._calculate_public_key_dh()
        self.shared_secret = None

        # Long-term signing parameters for MITM protection
        self.public_key_sign, self.private_key_sign = generate_signing_key_pair()

    def _calculate_public_key_dh(self):
        """Calculates the DH public key Y = G^a mod P."""
        return modular_exponentiation(self.G, self.private_exponent, self.P)

    def calculate_shared_secret(self, received_public_key):
        """Calculates the shared secret key K = Y_partner^a mod P."""
        if self.shared_secret is None:
            self.shared_secret = modular_exponentiation(
                received_public_key,
                self.private_exponent,
                self.P
            )
        return self.shared_secret

    def get_user_data(self):
        """Returns user data for table display."""
        return {
            "Subscriber": self.name,
            "Secret DH Exp (a)": self.private_exponent,
            "Public DH Key (Y)": self.public_key_dh,
            "Public Signing Key": self.public_key_sign  # This is shared/known by PKI
        }

    def sign_dh_key(self):
        """Signs the DH public key using the long-term private key."""
        return sign_message(self.private_key_sign, str(self.public_key_dh))

    def __str__(self):
        return self.name
