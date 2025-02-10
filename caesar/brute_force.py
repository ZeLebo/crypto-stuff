from cipher import caesar_cipher

def brute_force_caesar(cipher_text):
    results = []
    for key in range(26):
        decrypted_text = caesar_cipher(cipher_text, key, mode='decrypt')
        results.append((key, decrypted_text))
    return results

if __name__ == "__main__":
    cipher_text = "khoor"
    results = brute_force_caesar(cipher_text)
    for key, decrypted_text in results:
        print(f"Ключ {key}: {decrypted_text}")