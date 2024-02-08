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
        await client.send(
            client.build_message(
                method="private/get-order-history",
                params={
                    "instrument_name": "CRO_USDC",
                    "start_ts": 1587846300000,
                    "end_ts": 1587846358253,
                    "page_size": 0,
                    "page": 0
                }
            )
        )
        event = await client.next_event()
        print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
