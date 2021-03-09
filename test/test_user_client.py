from crypto_com import UserClient


def test_constructor():
    client = UserClient(api_secret="aa", api_key="bb")
    assert "wss://stream.crypto.com/v2/user" == client.api_url
    assert "aa".encode() == client.api_secret
    assert "bb" == client.api_key
