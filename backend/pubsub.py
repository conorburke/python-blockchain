import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

publish_key = 'pub-c-f7b598c3-2058-4110-83d3-f1ddfd5a91e6'
subscribe_key = 'sub-c-033d2ff0-8c31-11ea-8504-ea59babdc551'

pnconfig = PNConfiguration()
pnconfig.publish_key = publish_key
pnconfig.subscribe_key = subscribe_key
# pubnub = PubNub(pnconfig)

# TEST_CHANNEL = 'TEST_CHANNEL'
# BLOCK_CHANNEL = 'BLOCK_CHANNEL'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}

# async
# pubnub.subscribe().channels([TEST_CHANNEL]).execute()


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Incoming message: {message_object.channel} | {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n-- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n-- Did not replace chain: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n--Set the new transaction in the transaction pool')

# pubnub.add_listener(Listener())


class PubSub():
    """
    Handles publish/subscript layer of the app
    Provides comms between the nodes of the blockchain network
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """

        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        """

        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


if __name__ == '__main__':
    pubsub = PubSub()
    time.sleep(1)
    # pubnub.publish().channel(TEST_CHANNEL).message({'foo': 'bar'}).sync()

    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})