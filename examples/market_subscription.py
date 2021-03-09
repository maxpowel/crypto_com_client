from crypto_com.crypto_com import MarketClient
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def run():
    async with MarketClient() as client:
        await client.subscribe(["book.CRO_USDC.10"])
        while True:
            event = await client.next_event()
            print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
