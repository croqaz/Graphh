
#- rev: v1 -
#- hash: YAERSA -

from hashlib import blake2b

HASH_SIZE = 32


def hash(*data):
    """
    Blake2 64-bit hashing, 32 bytes output size.
    """
    key = blake2b(digest_size=HASH_SIZE)
    for d in data:
        if d is None or d == 'None' or d == 'NULL':
            d = b'null'
        elif isinstance(d, str):
            d = d.encode('utf8')
        elif isinstance(d, (int, float)):
            d = bytes(str(d).encode('utf8'))
        key.update(d)
    return key.digest()
