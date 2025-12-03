from user import User
from utils import get_public_params, display_table
from auth import verify_signature


class DiffieHellmanSimulator:
    def __init__(self):
        self.P, self.G = get_public_params()
        self.users = {}
        self.pki_keys = {}

    def setup_system(self, N=2):
        print(f"--- DH SYSTEM SETUP WITH AUTHENTICATION ({N} users) ---")

        self.users = {f"A{i+1}": User(f"A{i+1}") for i in range(N)}
        self.pki_keys = {name: user.public_key_sign for name,
                         user in self.users.items()}

        print("System Public Parameters:")
        print(f"  Modulus P = {self.P}")
        print(f"  Generator G = {self.G}")
        print("-" * 30)

        user_data = [user.get_user_data() for user in self.users.values()]
        display_table(user_data, "System Keys (PKI Public Keys are Known)")

    def run_authenticated_exchange(self, A: User, B: User, name_A, name_B):
        print(f"\n--- AUTHENTICATED DH PROTOCOL: {name_A} <-> {name_B} ---")

        # 1. A signs and sends
        signature_A = A.sign_dh_key()
        A_key = A.public_key_dh

        # 2. B verifies A
        A_pub_sign_key = self.pki_keys[name_A]
        is_A_verified, msg_A = verify_signature(
            A_pub_sign_key, str(A_key), signature_A)

        if not is_A_verified:
            print(f"AUTHENTICATION FAILURE: {
                  name_B} cannot verify {name_A}'s signature.")
            return False, None
        print(f"Verification by {name_B}: SUCCESS. ({msg_A})")

        # 3. B signs and sends
        signature_B = B.sign_dh_key()
        B_key = B.public_key_dh

        # 4. A verifies B
        B_pub_sign_key = self.pki_keys[name_B]
        is_B_verified, msg_B = verify_signature(
            B_pub_sign_key, str(B_key), signature_B)

        if not is_B_verified:
            print(f"AUTHENTICATION FAILURE: {
                  name_A} cannot verify {name_B}'s signature.")
            return False, None
        print(f"Verification by {name_A}: SUCCESS. ({msg_B})")

        # Key Calculation
        K_A = A.calculate_shared_secret(B_key)
        K_B = B.calculate_shared_secret(A_key)

        print(f"\n{name_A} calculated K_A = {K_A}")
        print(f"{name_B} calculated K_B = {K_B}")

        if K_A == K_B:
            print(f"RESULT: SUCCESS. Shared secret K_AB = {K_A}")
            return True, K_A
        else:
            print("RESULT: FAILURE. Keys do not match.")
            return False, None

    def test_successful_exchange(self):
        print("\n" + "="*80)
        print("TEST CASE 1: Successful Exchange (No MITM)")
        print("Expected: Both parties agree on the key.")
        print("="*80)

        A1 = self.users['A1']
        A2 = self.users['A2']

        self.run_authenticated_exchange(A1, A2, 'A1', 'A2')

    def test_mitm_attack(self):
        print("\n" + "="*80)
        print("TEST CASE 2: MITM Attack Simulation")
        print("Expected: Authentication fails when Eve substitutes her DH key.")
        print("="*80)

        A1 = self.users['A1']
        A2 = self.users['A2']

        # Eve setup (Eve generates her own independent signing and DH keys)
        Eve = User('Eve')

        # 1. A1 sends DH key A1_key and signature Sig_A1
        A1_key = A1.public_key_dh
        signature_A1 = A1.sign_dh_key()

        # 2. Eve intercepts. Eve substitutes A1_key with E_key, but must use A1's signature (Sig_A1)
        # to pretend she is A1.
        E_key = Eve.public_key_dh

        print("--- MITM SCENARIO START ---")
        print(f"A1 sends {A1_key} (signed by A1).")
        print(f"Eve intercepts and substitutes A1_key with E_key: {E_key}")

        # A2 receives E_key and signature_A1.

        A1_pub_sign_key = self.pki_keys['A1']

        # A2 attempts to verify the key received (E_key) using the signature received (signature_A1).
        # A2 uses A1's known public signing key (A1_pub_sign_key) to check if signature_A1
        # was created over E_key.

        is_verified, msg = verify_signature(
            A1_pub_sign_key,
            str(E_key),         # E_key is the substituted message content
            signature_A1        # signature_A1 is the signature created over A1_key
        )

        print(f"\nA2 attempts to verify E_key using A1's PKI key and A1's signature...")

        if is_verified:
            print(
                "RESULT: SECURITY FLAW: Authentication passed! (Check simulation logic)")
        else:
            print(
                f"RESULT: MITM BLOCKED. A2 detected forged key/signature mismatch. ({msg})")

        # Optional: Repeat the attack from B to A for completeness
        # B2_key = A2.public_key_dh
        # signature_B2 = A2.sign_dh_key()
        # A1_pub_sign_key = self.pki_keys['A2']
        # ...

        print("--- MITM SCENARIO END ---")


def main():
    simulator = DiffieHellmanSimulator()

    simulator.setup_system(N=2)

    simulator.test_successful_exchange()
    simulator.test_mitm_attack()

    print("\nTest suite terminated.")


if __name__ == '__main__':
    main()
