from pytest import raises

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    recipient_address = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient_address, amount)

    assert transaction.output[recipient_address] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_amount_exceeds_balance():
    with raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 5000)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)

    with raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new recipient', 5000)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first recipient'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    second_recipient = 'second recipient'
    second_amount = 75
    transaction.update(sender_wallet, second_recipient, second_amount)

    assert transaction.output[second_recipient] == second_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - second_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    to_first_again_amount = 25
    transaction.update(sender_wallet, first_recipient, to_first_again_amount)

    assert transaction.output[first_recipient] == first_amount + to_first_again_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - second_amount - to_first_again_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))

def test_valid_transaction_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 5000

    with raises(Exception, match='Invalid transaction. Output values.'):
        Transaction.is_valid_transaction(transaction)

def test_valid_transaction_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with raises(Exception, match='Invalid transaction. Invalid signature'):
        Transaction.is_valid_transaction(transaction)