import hashlib
import json

def crypto_hash(*args) -> str:
    """Produce a sha-256 hash for all the arguments

    Args:
        data ([type]): [description]

    Returns:
        str: resulting hash string
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    data_to_be_hashed = ''.join(stringified_args).encode('utf-8')
    return hashlib.sha256(data_to_be_hashed).hexdigest()


if __name__ == '__main__':
    print(f"crypto_hash('one', 2, [3], {{'four': 4\}}) - {crypto_hash('one', 2, [3], {'four': 4})}")
    print(f"crypto_hash(2, 'one', [3], {{'four': 4\}}) - {crypto_hash(2, 'one', [3], {'four': 4})}")