from backend.blockchain.block import Block

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

    def replace_chain(self, chain: list):
        """Replace the local chain with the incoming chain if the following applies:
               -> incoming chain must be longer than the local one
               -> incoming chain is valid

        Args:
            chain (list): incoming chain to compare to the current local chain
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace chain. Incoming chain is not longer than local chain")

        try :
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace chain. Incoming chain is invalid: {e}")

        self.chain = chain
    
    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'

    @staticmethod
    def is_valid_chain(chain: list):
        """Validate the incoming chain
        Enforce the following rules of the blockchaine:
            -> chain must start with genesis block
            -> blocks must be formatted correctly

        Args:
            chain ([array]): the chain of blocks that you want to validate
        """
        if chain[0] != Block.genesis():
            raise Exception('Genesis block must be valid')

        for i in range(1, len(chain)):
            cur_block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, cur_block)


if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain)
    blockchain.add_block('1234')
    print(blockchain)