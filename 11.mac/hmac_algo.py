import hashlib
import secrets
import binascii

H_LEN = 32
B_LEN = 64
IPAD = 0x36
OPAD = 0x5C
SECRET_KEY = secrets.token_bytes(32)


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    K_prime = key
    if len(key) > B_LEN:
        K_prime = hashlib.sha256(key).digest()
    if len(K_prime) < B_LEN:
        K_prime = K_prime + b'\x00' * (B_LEN - len(K_prime))

    print(f"{K_prime=}")

    ipad_bytes = bytes([IPAD] * B_LEN)
    opad_bytes = bytes([OPAD] * B_LEN)

    K_ipad = bytes([K_prime[i] ^ ipad_bytes[i] for i in range(B_LEN)])
    K_opad = bytes([K_prime[i] ^ opad_bytes[i] for i in range(B_LEN)])

    # Inner Hash = SHA256(K_ipad || M)
    inner_hash_input = K_ipad + message
    inner_hash = hashlib.sha256(inner_hash_input).digest()

    # Outer Hash = SHA256(K_opad || Inner Hash)
    outer_hash_input = K_opad + inner_hash
    final_mac_tag = hashlib.sha256(outer_hash_input).digest()

    return final_mac_tag


def verify_mac_manual(key: bytes, message: bytes, received_tag: bytes) -> bool:
    # to prevent time based attack gonna use safe method
    return secrets.compare_digest(hmac_sha256(key, message), received_tag)


def main():
    message_data = "HELLO WORLD".encode('utf-8')
    print(f"input message: {message_data.decode()}")
    print(f"key length: {len(SECRET_KEY)}")

    tag = hmac_sha256(SECRET_KEY, message_data)
    print(f"generated MAC: {binascii.hexlify(tag).decode()}")

    result_ok = verify_mac_manual(SECRET_KEY, message_data, tag)
    print(f"verification result is : {'SUCCESS' if result_ok else 'FAILURE'}")

    tampered_message = "HELLO WORLD.CHANGED".encode('utf-8')
    result_fail = verify_mac_manual(SECRET_KEY, tampered_message, tag)
    print(f"verification result is {'SUCCESS' if result_fail else 'FAILURE'}")


if __name__ == "__main__":
    main()
