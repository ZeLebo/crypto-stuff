# The electronic codes application
from service import Service


def readable(message, need_bytes=False, convert_to_bytes=False):
    shift = 40 if need_bytes else 80
    if need_bytes:
        if isinstance(message, int):
            message = message.to_bytes((message.bit_length() + 7) // 8, "big")
        return "\n".join([message[i:i + shift].hex() for i in range(0, len(message), shift)])
    if convert_to_bytes:
        return "\n".join([message[i:i + shift].encode().hex() for i in range(0, len(message), shift)])
    if isinstance(message, int):
        message = str(message)
    return "\n".join(message[i:i + shift] for i in range(0, len(message), shift))


def big_file():
    print("Testing on a big file")
    message = "abracadabra" * 100
    print(f"Message: abracadabra * 100\n")

    service = Service()
    public_key, private_key = service.generate_keys(1024)

    ciphertext = service.rsa.encrypt_big_file(message, public_key)
    text = service.rsa.decrypt_big_file(ciphertext, private_key)

    print(f"Encrypted message in bytes:\n{readable(ciphertext, need_bytes=True)}\n")
    print(f"Decrypted message: \n{readable(text, need_bytes=True)}\n")


def main():
    service = Service()
    public_key, private_key = service.generate_keys(1024)
    print(f"Public key:")
    print(readable(public_key[0]))
    print("=====================================")
    print(readable(public_key[1]))
    print()
    print(f"Private key:")
    print(readable(private_key[0]))
    print("=====================================")
    print(readable(private_key[1]))
    print()

    message = input("Enter a message to encrypt:\n")
    if len(message) == 0:
        message = "You had to fight the evil, not join it"
    print(f"Message: {message}\n")
    # print the message in bytes format
    print(f"Message in bytes:\n{readable(message, convert_to_bytes=True)}\n")

    ciphertext = service.encrypt(message, public_key)

    print(f"Encrypted message in bytes:\n{readable(ciphertext, need_bytes=True)}\n")

    signature = service.sign(message, private_key)
    print(f"Signature:\n{readable(signature)}\n")

    text = service.decrypt(ciphertext, private_key)
    if text:
        print(f"Decrypted message: {text}\n")
        print(f"Decrypted message in bytes:\n{readable(text, convert_to_bytes=True)}\n")

    try:
        res = service.verify(message, signature, public_key)
        print(f"Verification result: {res}")
    except Exception as e:
        print(f"Verification result: {e}")


if __name__ == '__main__':
    main()
    # main()
    # test_big()
