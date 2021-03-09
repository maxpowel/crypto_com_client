from crypto_com import UserClient
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

async def run():
    async with UserClient(
            api_key=os.environ["API_KEY"],
            api_secret=os.environ["API_SECRET"]
    ) as client:
        await client.authenticate()
        event = await client.next_event()
        print(event)
        while True:
            await client.subscribe(["user.trade"])
            print(event)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
