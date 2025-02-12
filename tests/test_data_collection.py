from src.data_collection.blockchain_client import BlockchainClient
from src.data_collection.wallet_fetcher import WalletFetcher


def test_blockchain_client_initialization():
    client = BlockchainClient()
    assert client.base_url == "https://api.etherscan.io/api"


def test_wallet_fetcher():
    fetcher = WalletFetcher()
    assert isinstance(fetcher.client, BlockchainClient)
