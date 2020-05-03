from backend.blockchain.block import Block

class Blockchain:
    """
    Blockchain: A public ledger of blocks
    Impl: A list of blocks; data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def replace_chain(self, incoming_chain):
        """
        Replace the local chain with incoming one if following rules:
        Incoming chain must be longer
        Incoming chain must be formatted properly
        """

        if len(incoming_chain) <= len(self.chain):
            raise Exception('Cannot replace chain. Incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(incoming_chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = incoming_chain

    def to_json(self):
        """
        Serialize to list of blocks
        """

        return [c.to_json() for c in self.chain]

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instance
        """

        blockchain = Blockchain()
        blockchain.chain = [Block.from_json(block_json) for block_json in chain_json]
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validates incoming chain.
        Enforce these rules:
        Chain starts with Genesis block
        Blocks must be formatted correctly.
        """

        if chain[0] != Block.genesis():
            raise Exception('Genesis must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)





if __name__ == '__main__':
    blockchain = Blockchain()

    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain.chain[2])