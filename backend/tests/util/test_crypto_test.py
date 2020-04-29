from backend.util.crypto_hash import crypto_hash


def test_crypto_hash():
    # tests to ensure that order doesn't matter
    assert crypto_hash(1, '2', [3]) == crypto_hash('2', 1, [3])
    assert crypto_hash('crazy') == '0ab599dd37527d71af9cb71e9326900d76f287d1c1afa9b61519e0a15497c961'
