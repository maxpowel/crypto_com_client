from crypto_com import MarketClient


def test_constructor():
    client = MarketClient()
    assert "wss://stream.crypto.com/v2/market" == client.api_url
