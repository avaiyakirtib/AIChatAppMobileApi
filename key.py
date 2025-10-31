import secrets
# Generate a 32-byte key (256 bits)
key = secrets.token_bytes(32)
print(key.hex()) # Print as hex string for easier use