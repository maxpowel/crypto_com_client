from crypto_com import CryptoClient
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

async def run():
    async with CryptoClient(
            client_type=CryptoClient.USER,
            channels=["user.trade"],
            api_key=os.environ["API_KEY"],
            api_secret=os.environ["API_SECRET"]
    ) as client:
        while True:
            event = await client.next_event()
            print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
