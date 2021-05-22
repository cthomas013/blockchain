import json

from uuid import uuid4
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from backend.config import STARTING_BALANCE

class Wallet():
    """An individual wallet for a miner.
    Keeps track of the miner's balance and allows the miner to authorize transactions.
    """

    def __init__(self) -> None:
        self.address = str(uuid4())[:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), 
            default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
    
    def sign(self, data):
        """Generate a signature based on the data using the local private key

        Args:
            data (): data to be signed
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        ))

    def serialize_public_key(self) -> str:
        """Reset the public key to its serialized version

        Returns:
            str: string representation of the public key
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    @staticmethod
    def verify(public_key, data, signature) -> bool:
        """Verify a sginature based on the public key and data

        Args:
            public_key (object): Elliptic Curve public key object
            data (any): original data
            signature (bytes): string of bytes

        Returns:
            bool: whether the signature is valid or not
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        # get the r and s values from the decoded signature
        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

if __name__ == '__main__':
    wallet = Wallet()
    print(f'wallet: {wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should be valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'should be invalid: {should_be_invalid}')
