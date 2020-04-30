import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINERATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'random test data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    # assert genesis.timestamp == GENESIS_DATA['timestamp']
    # assert genesis.last_hash == GENESIS_DATA['last_hash']
    # assert genesis.hash == GENESIS_DATA['hash']
    # assert genesis.data == GENESIS_DATA['data']

    for k, v in GENESIS_DATA.items():
        assert getattr(genesis, k) == v

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINERATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINERATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty == 1