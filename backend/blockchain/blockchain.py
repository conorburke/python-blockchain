from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet

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
        """
        The data needs to be a list if it is of the Transaction type
        """
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

        Blockchain.is_valid_transaction_chain(chain)


    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions
            - Each transaction must only appear once in the chain
            - There can only be one mining reward per block
            - Each transaction must be valid
        """

        transaction_ids = set()

        # for block in chain:
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                # if transaction.input == MINING_REWARD_INPUT:
                #     if has_mining_reward:
                #         raise Exception('There can only be one mining reward per block.' \
                #                         f'Check block with hash: {block.hash}')
                #     has_mining_reward = True

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('There can only be one mining reward per block.' \
                                        f'Check block with hash: {block.hash}')
                    has_mining_reward = True
                else:
                    # Seperate the mining reward blocks from other blocks for amount validation
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')

                Transaction.is_valid_transaction(transaction)


if __name__ == '__main__':
    blockchain = Blockchain()

    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain.chain[2])