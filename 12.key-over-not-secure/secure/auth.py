import secrets
import hashlib


def generate_signing_key_pair():
    private_key = secrets.token_hex(16)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()[:32]
    return public_key, private_key


def sign_message(private_key, message):
    """
    generates a signature marker based on the private key AND the message HASH
    """
    message_hash = hashlib.sha256(str(message).encode()).hexdigest()

    signature_marker = hashlib.sha256(
        f"{private_key}_{message_hash}".encode()).hexdigest()

    return f"SIG_{signature_marker}|HASH_{message_hash}"


def verify_signature(signer_public_key, original_message, signature):
    """
    verifies that the signature was created using the correct private key 
    over the exact message
    """

    if "SIG_" not in signature or "HASH_" not in signature:
        return False, "Signature structure invalid."

    received_hash = signature.split("|HASH_")[1]
    expected_hash = hashlib.sha256(str(original_message).encode()).hexdigest()

    if received_hash != expected_hash:
        return False, "Message hash mismatch. Key substitution detected."

    return True, "Signature verified."
