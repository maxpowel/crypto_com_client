"""The base client"""
import time
import hmac
import hashlib
import logging
from typing import List
# Pylint does not process __all__ correctly
# pylint: disable=E0611
from websockets import connect
from orjson import loads, dumps


logger = logging.getLogger("client")


class CryptoClient:
    """Base client. Just the raw protocol features"""

    def __init__(self, api_url):
        self._next_id = 1
        self.api_url = api_url
        self.websocket = None

    @staticmethod
    def get_nonce():
        """Get the next nonce. Currently is time based"""
        return int(time.time() * 1000)

    def next_id(self):
        """Incremental id"""
        i = self._next_id
        self._next_id += 1
        return i

    def build_message(self, method, params=None, **kwargs):
        """Base message structure"""
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

    async def send(self, message):
        """Serialize and send the message"""
        await self.websocket.send(dumps(message).decode())

    async def next_event(self):
        """Wait for the next websocket message"""
        next_message = None
        while next_message is None:
            next_message = loads(await self.websocket.recv())
            if next_message.get("method") == "public/heartbeat":
                next_message["method"] = "public/respond-heartbeat"
                next_message["nonce"] = self.get_nonce()
                logging.info("Heartbeat")
                await self.send(next_message)
                next_message = None
        return next_message

    async def __aenter__(self):
        logger.info("Connecting to %s", self.api_url)
        self.websocket = await connect(self.api_url)
        # The api documentation recommend to wait a second in order to void rate-limit error
        time.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc, atb):
        await self.websocket.close()

    async def subscribe(self, channels: List[str]):
        """Subscribe to the channels"""
        logger.info("Subscribing to %s", channels)
        await self.send(self.build_message(
            method="subscribe",
            params={"channels": channels}
        ))


class AuthenticatedClient(CryptoClient):
    """Client for private user operations"""

    def __init__(self, api_key, api_secret, api_url):
        super().__init__(api_url)
        self.api_secret = api_secret.encode()
        self.api_key = api_key

    def sign_message(self, message: dict):
        """Sign message using the crypto com method"""
        message_to_sig = message["method"] + str(message["id"]) + self.api_key + str(message["nonce"])
        message["sig"] = hmac.new(self.api_secret, msg=message_to_sig.encode(), digestmod=hashlib.sha256).hexdigest()
        return message

    async def authenticate(self):
        """Perform authentication"""
        logger.info("Authenticating...")
        await self.send(self.build_message(
            method="public/auth",
            api_key=self.api_key
        ))

    async def send(self, message):
        """Serialize and send the message"""
        await self.websocket.send(dumps(self.sign_message(message)))


class MarketClient(CryptoClient):
    """Client for public operations"""

    def __init__(self, api_url="wss://stream.crypto.com/v2/market"):
        super().__init__(api_url)


class UserClient(AuthenticatedClient):
    """Client for user operations"""

    def __init__(self, api_key, api_secret, api_url="wss://stream.crypto.com/v2/user"):
        super().__init__(api_key=api_key, api_secret=api_secret, api_url=api_url)
