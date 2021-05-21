from backend.wallet.wallet import Wallet

def test_verify_valid_signature():
    data = {
        'foo': 'test data'
    }
    
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature) 

def test_verify_invalid_signature_bad_public_key():
    data = {
        'foo': 'test data'
    }
    
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)

def test_verify_invalid_signature_bad_data():
    data = {
        'foo': 'test data'
    }
    
    wallet = Wallet()
    signature = wallet.sign(data)

    bad_data = {
        'foo': 'bad data'
    }

    assert not Wallet.verify(wallet.public_key, bad_data, signature)