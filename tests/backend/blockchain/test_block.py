import time

from pytest import (
    raises,
    fixture
)
from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block=last_block, data=data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0 : block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1

@fixture
def last_block():
    return Block.genesis()

@fixture
def block(last_block):
    return Block.mine_block(last_block, 'test-data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'bad last hash'
    with raises(Exception, match='last_hash must be correct'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    with raises(Exception, match='Proof of work requirement not met'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}1111abc'

    with raises(Exception, match='Block difficulty must only adjust by 1'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '000000000000000001bf4dcf561'
    with raises(Exception, match='hash does not match'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash_changed_timestamp(last_block, block):
    block.timestamp += 1
    with raises(Exception, match='hash does not match'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash_changed_data(last_block, block):
    block.data = 'trst_data'
    with raises(Exception, match='hash does not match'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash_changed_difficulty(last_block, block):
    block.data = 'trst_data'
    with raises(Exception, match='hash does not match'):
        Block.is_valid_block(last_block, block)

def test_is_vaild_block_bad_nonce(last_block, block):
    block.nonce += 1
    with raises(Exception, match='hash does not match'):
        Block.is_valid_block(last_block, block)