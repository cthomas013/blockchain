import time

from pluggy.manager import DistFacade

from backend.utils.crypto_hash import crypto_hash
from backend.utils.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}

class Block:
    """
    Block: a unit of storage
    Store transactions in the blockchain that supports a cryptocurrency
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce) -> None:
        """Initialize the block

        Args:
            timestamp (integer): epoch nanosecond timestamp of when the block is being created
            last_hash (string): hash string for the previous block
            hash (string): hash of the current lock's data
            data (string): data to be stored in the block
        """
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def to_json(self) -> dict:
        """Serialize the block object into a dictionary

        Returns:
            dict: dictionary representation of the fields in the block
        """
        return self.__dict__

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, o: object) -> bool:
        return self.__dict__ == o.__dict__
    
    @staticmethod
    def mine_block(last_block, data) -> object:
        """Function to mine a block in the blockchain until a block hash is found that meets
        the difficulty leading zeroes proof of work requirement

        Args:
            last_block (Block): the last block in the chain
            data (string): data for the new block

        Returns:
            object: new Block object that has been mined
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0 : difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)        

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis() -> object:
        """Generate the genesis block

        Returns:
            object: return a block object to be the genesis block in the chain
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json) -> object:
        """Creates a block object from json

        Args:
            block_json (json): json representation of a block's data

        Returns:
            object: a Block object that has been created from the relevant json data
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp) -> int:
        """This will adjust the proof of work difficulty based on the time it took to mine blocks.
        The difficulty will be increased if a block has been mined tooo quickly and decrease the difficulty
        if blocks are being mined too slowly

        Args:
            last_block ([type]): [description]
            new_timestamp ([type]): [description]
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        
        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """Validate block by enforcing the following rules:
             --> block must have the proper last_hash reference
             --> block must meet the proof of work requirement
             --> the difficulty must only adjust by 1
             --> block hash must be valid based on the block fields

        Args:
            last_block ([type]): [description]
            block ([type]): [description]
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')
        
        if hex_to_binary(block.hash)[0 : block.difficulty] != '0' * block.difficulty:
            raise Exception('Proof of work requirement not met')

        if abs(last_block.difficulty - block.difficulty) > 1 :
            raise Exception('Block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        # if hex_to_binary(reconstructed_hash)[0 : block.difficulty] != '0' * block.difficulty:
        #     raise Exception('Nonce value does not produce proper proof of work requirement')

        if block.hash != reconstructed_hash:
            raise Exception('Block hash does not match')


if __name__ == '__main__':
    genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, 'foo')
    # print(block)

    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil-data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')