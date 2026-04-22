from tronpy.keys import PrivateKey

from app.core.settings import get_setting


class SigningService:
    def __init__(self):
        private_key_hex = get_setting("TRON_PRIVATE_KEY").strip().strip('"').strip("'")
        self.private_key = PrivateKey(bytes.fromhex(private_key_hex))

    def sign_transaction(self, txn):
        return txn.sign(self.private_key)