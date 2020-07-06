import json
import websockets
import hmac
import hashlib
import time
import logging
from typing import List


class CryptoClient(object):

    MARKET = 0
    USER = 1

    MARKET_URI = "wss://stream.crypto.com/v2/market"
    USER_URI = "wss://stream.crypto.com/v2/user"

    def get_nonce(self):
        return int(time.time() * 1000)

    def __init__(self, client_type: int, channels: List[str] = None, api_secret: str = None, api_key: str = None, websocket=None, json_encoder=json.dumps, json_decoder=json.loads, ):
        self.api_secret = api_secret.encode() if api_key else None
        self.api_key = api_key
        self._next_id = 1
        self.dumps = json_encoder
        self.loads = json_decoder
        self.channels = channels
        self.websocket = websocket
        self.client_type = client_type
        self.logger = logging.getLogger("crypto_com")

    def next_id(self):
        i = self._next_id
        self._next_id += 1
        return i

    async def authenticate(self):
        self.logger.info("Authenticating...")
        await self.send(self.sign_message(self.build_message(
            method="public/auth",
            api_key=self.api_key
        )))

    async def send(self, message):
        await self.websocket.send(self.dumps(message))

    def build_message(self, method, params=None, **kwargs):
        message = {
            "id": self.next_id(),
            "method": method,
            "nonce": self.get_nonce()
        }
        if params:
            message["params"] = params

        if kwargs:
            message.update(kwargs)
        return message

    def sign_message(self, message):
        message_to_sig = message["method"] + str(message["id"]) + self.api_key + str(message["nonce"])
        message["sig"] = hmac.new(self.api_secret, msg=message_to_sig.encode(), digestmod=hashlib.sha256).hexdigest()
        return message

    async def next_event(self):
        r = None
        while r is None:
            r = await self.parse_message(json.loads(await self.websocket.recv()))
        return r

    async def subscribe(self):
        self.logger.info("Subscribing...")
        await self.send(self.build_message(
            method="subscribe",
            params={"channels": self.channels}
        ))

    async def parse_message(self, data):
        if data["method"] == "public/heartbeat":
            data["method"] = "public/respond-heartbeat"
            logging.info("Heartbeat")
            await self.send(data)
        elif data["method"] == "subscribe":
            res = data.get("result")
            if res:
                return res
            else:
                if data["code"] == 0:
                    self.logger.info("Subscription success!")
                else:
                    raise Exception(f"Error when subscribing: {json.dumps(data)}")
        elif data["method"] == "public/auth":
            if data["code"] == 0:
                self.logger.info("Authentication success!")
                if self.channels:
                    await self.subscribe()
            else:
                raise Exception(f"Auth error: {json.dumps(data)}")
        else:
            return data

    async def __aenter__(self):
        self.websocket = await websockets.connect(self.MARKET_URI if self.MARKET == self.client_type else self.USER_URI)
        if self.client_type == self.USER:
            await self.authenticate()
        elif self.channels:
            await self.subscribe()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.websocket.close()
