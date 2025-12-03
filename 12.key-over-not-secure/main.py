from user import User
from utils import get_public_params, display_table


class DiffieHellmanSimulator:
    def __init__(self):
        self.users = {}
        self.P, self.G = get_public_params()

    # Sets up users, generates keys, and displays the parameter table
    def setup_system(self, N):
        print(f"--- DH SYSTEM SETUP ({N} users) ---")

        self.users = {f"A{i+1}": User(f"A{i+1}") for i in range(N)}

        print("System Public Parameters:")
        print(f"  Modulus P = {self.P}")
        print(f"  Generator G = {self.G}")
        print("-" * 30)

        user_data = [user.get_user_data() for user in self.users.values()]
        display_table(user_data, "Generated Keys and Parameters")

    def run_exchange(self, name_A, name_B):
        """Executes the DH protocol between two selected subscribers."""

        A = self.users.get(name_A)
        B = self.users.get(name_B)

        if not A or not B:
            print("Error: One or both subscribers do not exist.")
            return

        print(f"\n--- DH KEY EXCHANGE PROTOCOL: {name_A} <-> {name_B} ---")

        print(f"1. {name_A} (Secret a={
              A.private_exponent}) calculates public key A = G^a mod P:")
        print(f"   A = {self.G}^{A.private_exponent} mod {
              self.P} = {A.public_key}")
        print(f"   {name_A} sends {A.public_key} to {name_B}")

        print(f"2. {name_B} (Secret b={
              B.private_exponent}) calculates public key B = G^b mod P:")
        print(f"   B = {self.G}^{B.private_exponent} mod {
              self.P} = {B.public_key}")
        print(f"   {name_B} sends {B.public_key} to {name_A}")

        K_A = A.calculate_shared_secret(B.public_key)
        print(f"\n3. {name_A} receives {
              B.public_key} and calculates the shared secret K_A:")
        print(f"   K_A = B^a mod P = {B.public_key}^{
              A.private_exponent} mod {self.P} = {K_A}")

        K_B = B.calculate_shared_secret(A.public_key)
        print(f"4. {name_B} receives {
              A.public_key} and calculates the shared secret K_B:")
        print(f"   K_B = A^b mod P = {A.public_key}^{
              B.private_exponent} mod {self.P} = {K_B}")

        print("\n=======================================================")
        if K_A == K_B:
            print(f"SUCCESS: Shared secret key K_AB = {K_A}")
        else:
            print("FAILURE: Keys do not match.")
        print("=======================================================")


def main():
    simulator = DiffieHellmanSimulator()

    while True:
        try:
            N = int(input("Enter the number of users (N >= 2): "))
            if N >= 2:
                break
            else:
                print("Please enter a number >= 2.")
        except ValueError:
            print("Invalid input. Try again.")

    simulator.setup_system(N)
    user_list = list(simulator.users.keys())

    while True:
        print("\n--- Menu ---")
        print(f"Available users: {', '.join(user_list)}")
        print("Enter 'exit' to terminate.")

        selection = input(
            "Select two subscribers for key exchange (example: A1,A3): ").strip()

        if selection.lower() == 'exit':
            break

        try:
            if ',' not in selection:
                print("Invalid format. Use a comma (example: A1,A2).")
                continue

            A_name, B_name = [name.strip() for name in selection.split(',')]

            if A_name not in user_list or B_name not in user_list or A_name == B_name:
                print("Invalid selection or identical subscribers. Try again.")
                continue

            simulator.run_exchange(A_name, B_name)

        except Exception as e:
            print(f"An error occurred during the exchange: {e}")


if __name__ == '__main__':
    main()
