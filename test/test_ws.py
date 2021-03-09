import asyncio
import websockets
from crypto_com.crypto_com import CryptoClient, AuthenticatedClient
import json

def run_t(server, test_code):
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(
        websockets.serve(server, 'localhost', 8765))
    loop.run_until_complete(test_code())
    server.close()


async def send_server(websocket, path):
    async for message in websocket:
        await websocket.send('{"hi": "bar"}')
        await websocket.close()


async def send():
    async with CryptoClient(api_url="ws://localhost:8765") as client:
        await client.send({"hi": "foo"})
        response = await client.next_event()
        assert response["hi"] == "bar"

def test_send():
    run_t(server=send_server, test_code=send)


# Subscribe
async def subscribe_server(websocket, path):
    async for message in websocket:
        m = json.loads(message)
        if m["method"] == "subscribe":
            await websocket.send(json.dumps({"id": m["id"] + 1, "code": 0, "method": "subscribe"}))
        else:
            await websocket.send(json.dumps({"id": m["id"] + 1, "code": 1, "method": m["method"]}))
        await websocket.close()


async def subscribe():
    async with CryptoClient(api_url="ws://localhost:8765") as client:
        await client.subscribe(channels=["test"])
        event = await client.next_event()
        assert event["code"] == 0
        assert event["method"] == "subscribe"

def test_subscribe():
    run_t(server=subscribe_server, test_code=subscribe)



async def send_authenticated_server(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        await websocket.close()


async def send_authenticated():
    async with AuthenticatedClient(api_url="ws://localhost:8765", api_key="my_key", api_secret="my_secret") as client:
        await client.send({"method": "foo", "id": 2, "nonce": 1})
        response = await client.next_event()
        signed = {'method': 'foo', 'id': 2, 'nonce': 1, 'sig': '686978ec793e35bef9c01ef80250ceb3c061dd994ea1e917e10f3e7be9f75ff4'}
        assert signed == response

def test_send_authenticated():
    run_t(server=send_authenticated_server, test_code=send_authenticated)


async def authenticate_server(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        await websocket.close()


async def authenticate():
    async with AuthenticatedClient(api_url="ws://localhost:8765", api_key="my_key", api_secret="my_secret") as client:
        # Monkey path to put a predictable nonce
        client.get_nonce = lambda: 0
        await client.authenticate()
        response = await client.next_event()
        assert "public/auth" == response["method"]
        assert "37273bcc50b927ba2518d1cf0c773c089cddca2357a56403ba769baf1bfc76cc" == response["sig"]


def test_authenticate():
    run_t(server=authenticate_server, test_code=authenticate)


async def heartbeat_server(websocket, path):
    await websocket.send(json.dumps({"method": "public/heartbeat"}))
    heartbeat_response = json.loads(await websocket.recv())
    assert heartbeat_response["method"] == "public/respond-heartbeat"
    await websocket.send(json.dumps({"method": "close"}))
    await websocket.close()


async def heartbeat():
    async with CryptoClient(api_url="ws://localhost:8765") as client:
        response = await client.next_event()


def test_heartbeat():
    run_t(server=heartbeat_server, test_code=heartbeat)
