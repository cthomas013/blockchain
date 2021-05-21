from uuid import uuid4
from time import time_ns

from backend.wallet.wallet import Wallet

class Transaction:
    """Document an exchange in currency from a sender to one or more recepients
    """

    def __init__(self, sender_wallet, recipient, amount) -> None:
        self.id = str(uuid4())[:8]
        self.output = self.create_output(sender_wallet, recipient, amount)
        self.input = self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount) -> dict:
        """Structure the output data for the transaction

        Args:
            sender_wallet ([type]): [description]
            recipient ([type]): [description]
            amount ([type]): [description]

        Returns:
            dict: dictionary representing the output data for a transaction
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input(self, sender_wallet, output) -> dict:
        """Structure the input data for the transaction. This will also include the signature of the sender wallet.

        Args:
            sender_wallet ([type]): [description]
            output ([type]): [description]

        Returns:
            dict: dictionary containing all of the inpt data for a transaction
        """
        return {
            'timestamp': time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        """Will update the transaction with an existing or new recipient

        Args:
            sender_wallet ([type]): [description]
            recipient ([type]): [description]
            amount ([type]): [description]
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else :
            self.output[recipient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    @staticmethod
    def is_valid_transaction(transaction):
        """Validate a transaction. Will raise an exception if the transaction is not valid.

        Args:
            transaction (object): transaction object to be validated
        """
        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction. Output values.')

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid transaction. Invalid signature')

if __name__ == '__main__':
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction : {transaction.__dict__}')

