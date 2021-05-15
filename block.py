import time

from crypto_hash import crypto_hash

class Block:
    """
    Block: a unit of storage
    Store transactions in the blockchain that supports a cryptocurrency
    """

    def __init__(self, timestamp, last_hash, hash, data) -> None:
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

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data})'
        )
    
    @staticmethod
    def mine_block(last_block, data) -> object:
        """Function to mine a block in the blockchain

        Args:
            last_block (Block): the last block in the chain
            data (string): data for the new block

        Returns:
            object: new Block object that has been mined
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis() -> object:
        """Generate the genesis block

        Returns:
            object: return a block object to be the genesis block in the chain
        """
        return Block(1, 'genesis_last_hash', 'genesis_hash', [])


if __name__ == '__main__':
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(block)