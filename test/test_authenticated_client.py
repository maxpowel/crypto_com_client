from crypto_com.crypto_com import AuthenticatedClient


def test_constructor():
    client = AuthenticatedClient(api_url="my_url", api_key="my_key", api_secret="my_secret")
    assert "my_url" == client.api_url
    assert "my_key" == client.api_key
    assert "my_secret".encode() == client.api_secret

