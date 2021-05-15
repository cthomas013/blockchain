from block import Block

class Blockchain:
    """
    Blockchain: a public ledger of transactions
    Implemented as a array of blocks --> data sets of transactions
    """

    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def add_block(self, data) -> None:
        """Add a block to the chain

        Args:
            data (string): data to be stored in the block
        """
        self.chain.append(Block.mine_block(self.chain[-1], data))
    
    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'

if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain)
    blockchain.add_block('1234')
    print(blockchain)