from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class StellarClient:
    def __init__(self):
        self.server = Server(settings.STELLAR_SERVER)
        self.network = settings.STELLAR_NETWORK

    def create_account(self):
        """Generate new Stellar keypair"""
        keypair = Keypair.random()
        return {
            'public_key': keypair.public_key,
            'secret_key': keypair.secret,
        }

    def fund_testnet_account(self, public_key):
        """Fund account on testnet"""
        try:
            response = requests.get(
                f'https://friendbot.stellar.org?addr={public_key}'
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to fund account: {e}")
            return False

    def anchor_hash(self, trade_hash, keypair):
        """Store trade hash on Stellar ledger"""
        try:
            source_account = self.server.load_account(keypair.public_key)
            
            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    base_fee=100,
                    network_passphrase=self.network,
                )
                .add_text_memo(trade_hash[:28])
                .set_timeout(300)
                .build()
            )
            
            transaction.sign(keypair)
            response = self.server.submit_transaction(transaction)
            return response.get('hash')
        except Exception as e:
            logger.error(f"Failed to anchor hash: {e}")
            return None

    def mint_performance_token(self, user_keypair, win_rate):
        """Mint SBT for performance proof"""
        try:
            source_account = self.server.load_account(user_keypair.public_key)
            
            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    base_fee=100,
                    network_passphrase=self.network,
                )
                .add_text_memo(f"WR:{int(win_rate)}")
                .set_timeout(300)
                .build()
            )
            
            transaction.sign(user_keypair)
            response = self.server.submit_transaction(transaction)
            return response.get('hash')
        except Exception as e:
            logger.error(f"Failed to mint token: {e}")
            return None
