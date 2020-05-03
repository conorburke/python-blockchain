import os
import random
import requests
from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

# for i in range(3):
#     blockchain.add_block(i)

@app.route('/')
def default():
    return 'welcome to bc'


@app.route('/blockchain')
def route_blockchain():
    # return blockchain.__repr__()
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'transaction data'

    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result, result.json: {result}, {result.json()}')

    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n-- successfully synced the local chain')
    except Exception as e:
        print(f'\n-- Error syncing new chain: {e} ')
app.run(port=PORT)