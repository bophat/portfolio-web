"""
URL encoding utilities for public user IDs.
Uses base62 encoding for short, URL-safe IDs.
"""
import hashlib
import string

# Base62 character set (URL-safe)
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(ALPHABET)

# Salt for encoding (change in production!)
SALT = "portfolio_secret_salt_2024"


def encode_user_id(user_id: int) -> str:
    """
    Encode a user ID to a short, URL-safe string.
    Uses XOR with a hash-derived key for obfuscation.
    
    Example: 1 -> "aX83kZ"
    """
    # Create a numeric key from salt
    hash_obj = hashlib.sha256(SALT.encode())
    key = int(hash_obj.hexdigest()[:8], 16)
    
    # XOR the user_id with key for obfuscation
    obfuscated = user_id ^ key
    
    # Convert to base62
    if obfuscated == 0:
        return ALPHABET[0]
    
    result = []
    while obfuscated > 0:
        result.append(ALPHABET[obfuscated % BASE])
        obfuscated //= BASE
    
    return ''.join(reversed(result))


def decode_user_id(public_id: str) -> int:
    """
    Decode a public ID back to the original user ID.
    
    Example: "aX83kZ" -> 1
    """
    # Convert from base62 to number
    obfuscated = 0
    for char in public_id:
        obfuscated = obfuscated * BASE + ALPHABET.index(char)
    
    # Create the same key from salt
    hash_obj = hashlib.sha256(SALT.encode())
    key = int(hash_obj.hexdigest()[:8], 16)
    
    # XOR again to get original ID
    return obfuscated ^ key


def generate_public_id_for_user(user_id: int) -> str:
    """
    Generate and return a public ID for a user.
    This is the main function to call when creating a user.
    """
    return encode_user_id(user_id)
