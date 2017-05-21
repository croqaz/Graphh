
from hashlib import blake2b

def hash(*data):
    key = blake2b(digest_size=32)
    for d in data:
        if d is None or d == 'None' or d == 'NULL':
            d = b'null'
        elif isinstance(d, str):
            d = d.encode('utf8')
        elif isinstance(d, (int, float)):
            d = bytes(str(d).encode('utf8'))
        key.update(d)
    return key.digest()
