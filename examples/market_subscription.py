from crypto_com import CryptoClient
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def run():
    async with CryptoClient(
            client_type=CryptoClient.MARKET,
            channels=[
                "book.CRO_USDC.10"
            ]
    ) as client:
        while True:
            event = await client.next_event()
            print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
