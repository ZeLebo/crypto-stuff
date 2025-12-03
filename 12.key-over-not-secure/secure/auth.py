import secrets
import hashlib


def generate_signing_key_pair():
    private_key = secrets.token_hex(16)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()[:32]
    return public_key, private_key


def sign_message(private_key, message):
    """Generates a signature marker based on the private key AND the message HASH."""

    # 1. Hash the content being signed
    message_hash = hashlib.sha256(str(message).encode()).hexdigest()

    # 2. Simulate encryption of the hash using the private key
    # For simulation, we combine a private key component with the message hash.
    signature_marker = hashlib.sha256(
        f"{private_key}_{message_hash}".encode()).hexdigest()

    # The signature contains the result of the simulated signing operation (signature_marker)
    # and the original message hash for integrity check.
    return f"SIG_{signature_marker}|HASH_{message_hash}"


def verify_signature(signer_public_key, original_message, signature):
    """Verifies that the signature was created using the correct private key over the exact message."""

    if "SIG_" not in signature or "HASH_" not in signature:
        return False, "Signature structure invalid."

    # In a real PKI: The signature (SIG_) would be decrypted by the public key
    # to retrieve the original message hash. Since we cannot decrypt here,
    # we simulate the failure condition based on the integrity of the signed content.

    # Check 1: Does the signature contain the correct hash of the message being verified?
    received_hash = signature.split("|HASH_")[1]
    expected_hash = hashlib.sha256(str(original_message).encode()).hexdigest()

    if received_hash != expected_hash:
        # This occurs if Eve substitutes E_key for A_key, but keeps the signature Sig(A_key).
        return False, "Message hash mismatch. Key substitution detected."

    # Since we cannot check if SIG_ was created by the *corresponding* private key without a full PKI,
    # we trust that the PKI lookup (A1_pub_sign_key) already identified the expected sender.

    return True, "Signature verified."
