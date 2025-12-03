import random

P_PRIME = random.choice([307, 311, 313, 317, 331, 337, 379, 383, 389, 397])
G_GENERATOR = random.randint(1, P_PRIME)


def get_public_params():
    return P_PRIME, G_GENERATOR


def modular_exponentiation(base, exponent, modulus):
    return pow(base, exponent, modulus)


def generate_secret_exponent(p):
    return random.randint(2, p - 2)


def display_table(data_list, title):
    print(f"\n--- {title} ---")
    if not data_list:
        print("No data to show table")
        return

    headers = list(data_list[0].keys())
    widths = {h: max(len(h), max(len(str(d.get(h, '')))
                     for d in data_list)) for h in headers}

    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    print(header_line)
    print("-" * len(header_line))

    for row in data_list:
        print(" | ".join(str(row.get(h, '')).ljust(
            widths[h]) for h in headers))
    print("-" * len(header_line))
