import time
from backend.util.crypto_hash import crypto_hash

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'glh',
    'hash': 'gh',
    'data': []
}

class Block:
    """
    A unit of storage
    """

    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return (
            f'Block - data: {self.data}'
            f'timestamp: {self.timestamp}'
            f'last_hash: {self.last_hash}'
            f'hash: {self.hash}'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mines a block based on last block and new input (data)

        returns a Block
        """

        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Generate the genesis block
        """

        # return Block(GENESIS_DATA['timestamp'], GENESIS_DATA['last_hash'], GENESIS_DATA['hash'], GENESIS_DATA['data'])
        return Block(**GENESIS_DATA)


if __name__ == '__main__':
    print('Block exectuion')
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foobar')
    print(block)