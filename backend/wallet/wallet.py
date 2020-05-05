import uuid
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature

from backend.config import STARTING_BALANCE


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of miner's balance.
    Allows miner to authorize transactions.
    """

    def __init__(self, blockchain=None):
        self.address = str(uuid.uuid4())[0:8]
        # self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
        self.blockchain = blockchain

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)


    def sign(self, data):
        """
        Generates a signatuare based on the data using the local private key
        """

        # data has to be bytes-like, so use json.dumps and then encode it
        return decode_dss_signature(
            self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
        )

    def serialize_public_key(self):
        """
        Serialize the public key to its serialized version to send over HTTP
        """

        self.public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # print(f'self.public_key_bytes: {self.public_key_bytes}')

        decoded_public_key = self.public_key_bytes.decode('utf-8')
        # print(f'\ndecoded public key: {decoded_public_key}')

        self.public_key = decoded_public_key


    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the public key and the data
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        # print(f'\nsignature: {signature}')
        (r, s) = signature

        try:
            # public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            # deserialized_public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            deserialized_public_key.verify(encode_dss_signature(r, s), json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

            return True
        except InvalidSignature:
            return False


    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calculate the balance of the given address considering the transaction data within the blockchain
        The balance is found by adding the output values that belong to the address since the most recent
        transaction by that address
        """

        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    # Any time the address conducts a new transaction it resets its balance
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance

if __name__ == '__main__':
    wallet = Wallet()
    print(f'wallet: {wallet.__dict__}')

    data = {'foo': 'bar'}

    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should be valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'should be invalid: {should_be_invalid}')


