import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-64c7cc2c-b9d9-11eb-8f6a-ae5fdf7280c3'
pnconfig.publish_key = 'pub-c-c576abd6-9901-4719-939f-44029b785c6e'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool) -> None:
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel : {message_object.channel} | Message : {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n --  Did not replace chain: {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)

            print('\n -- New transaction has been set in the transaction pool')


class PubSub():
    """Handles the publish/subscirbe layer of the application.
    Provides communication between the nodes of the blockchain
    """
    def __init__(self, blockchain, transaction_pool) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """Publish message object to the channel

        Args:
            channel (string): the channel you want to publish the message to
            message (object): message object that you want to publish
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """Will broadcast a blcok object to all the nodes

        Args:
            block (object): Block object
        """
        self.pubnub.publish().channel(CHANNELS['BLOCK']).message(block.to_json()).sync()

    def broadcast_transaction(self, transaction):
        """Will broadcast a transaction to all nodes

        Args:
            transaction (object): transaction object to be sent to the transaction channel 
        """
        self.pubnub.publish().channel(CHANNELS['TRANSACTION']).message(transaction.to_json()).sync()

if __name__ == '__main__':
    pubsub =PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], { 'foo': 'bar' })
