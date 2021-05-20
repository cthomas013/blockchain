from pytest import (
    fixture,
    raises
)

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block, GENESIS_DATA

def test_blockchain():
    blockchain = Blockchain()

    assert isinstance(blockchain, Blockchain)
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data

@fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    
    return blockchain


def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'test-bad-hash'

    with raises(Exception, match='Genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_is_valid_chain_bad_block(blockchain_three_blocks):
    blockchain_three_blocks.chain[2].hash = 'test-bad-hash'

    with raises(Exception):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)

    assert blockchain.chain == blockchain_three_blocks.chain

def test_replace_chain_shorter_chain(blockchain_three_blocks):
    blockchain = Blockchain()

    with raises(Exception, match="Cannot replace chain. Incoming chain is not longer than local chain"):
        blockchain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_block_in_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'bad-hash'

    with raises(Exception, match="Cannot replace chain. Incoming chain is invalid"):
        blockchain.replace_chain(blockchain_three_blocks.chain)
