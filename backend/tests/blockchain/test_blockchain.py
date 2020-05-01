import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_blcok():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_three_blocks():
    bc = Blockchain()

    for i in range(3):
        bc.add_block(i)

    return bc


def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'evil hash'

    with pytest.raises(Exception, match='Genesis must be valid'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_replace_chain(blockchain_three_blocks):
    bc = Blockchain()
    bc.replace_chain(blockchain_three_blocks.chain)

    assert bc.chain == blockchain_three_blocks.chain


def test_replace_chain_chain_not_longer(blockchain_three_blocks):
    bc = Blockchain()

    with pytest.raises(Exception, match='Cannot replace chain. Incoming chain must be longer'):
        blockchain_three_blocks.replace_chain(bc.chain)


def test_replace_chain_chain_is_invalid(blockchain_three_blocks):
    bc = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'evil hash'

    with pytest.raises(Exception, match='Cannot replace. The incoming chain is invalid'):
        bc.replace_chain(blockchain_three_blocks.chain)