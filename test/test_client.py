from crypto_com.crypto_com import CryptoClient
import time

def test_constructor():
    client = CryptoClient(api_url="my_api")
    assert "my_api" == client.api_url

def test_nonce():
    nonce = CryptoClient.get_nonce()
    time.sleep(1)
    next_nonce = CryptoClient.get_nonce()
    assert nonce < next_nonce


def test_next_id():
    client = CryptoClient(api_url="")
    assert 1 == client.next_id()
    assert 2 == client.next_id()
    assert 3 == client.next_id()
    assert 4 == client.next_id()
    assert 5 == client.next_id()
    assert 6 == client.next_id()


def test_build_message():
    # Simple message
    client = CryptoClient(api_url="my_api")
    message_1 = client.build_message("my_method")
    assert 3 == len(message_1)
    assert "my_method" == message_1["method"]
    assert 0 < message_1["nonce"]
    assert 1 == message_1["id"]
    time.sleep(0.5)
    # With params
    params = {"p1": 3, "p2": "test", "p3": {"d": 1, "l": [1, 2]}}
    message_2 = client.build_message("my_method_params", params=params)
    assert 4 == len(message_2)
    assert "my_method_params" == message_2["method"]
    assert message_1["nonce"] < message_2["nonce"]
    assert 2 == message_2["id"]
    assert params == message_2["params"]
    time.sleep(0.5)
    # With extra args
    message_3 = client.build_message("my_method_args", my="value", foo="bar")
    assert 5 == len(message_3)
    assert "my_method_args" == message_3["method"]
    assert message_2["nonce"] < message_3["nonce"]
    assert 3 == message_3["id"]
    assert message_3["my"] == "value"
    assert message_3["foo"] == "bar"
    time.sleep(0.5)
    # With params and extra args
    message_4 = client.build_message("my_method_all", params=params, my2="value", foo2="bar")
    assert 6 == len(message_4)
    assert "my_method_all" == message_4["method"]
    assert message_3["nonce"] < message_4["nonce"]
    assert 4 == message_4["id"]
    assert message_4["my2"] == "value"
    assert message_4["foo2"] == "bar"
    assert params == message_4["params"]

