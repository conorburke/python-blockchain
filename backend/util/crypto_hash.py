import hashlib
import json


def crypto_hash(*args):
    """
    return: a sha-256 hash of the parameters
    """
    data = [json.dumps(a) for a in args]
    data = sorted(data)
    # data = json.dumps(args)
    data = ''.join(data)
    data = json.dumps(data)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print(f"{crypto_hash(1, '2', [3])}")
    print(f"{crypto_hash('2', 1, [3])}")
