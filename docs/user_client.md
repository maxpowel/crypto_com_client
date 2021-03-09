# User Client

You can use this client to access the public data. You can subscribe to tickers, trades...

In this example we are creating an order, and the listing open orders.

```python
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
        await client.send(
            client.build_message(
                method="private/create-order",
                params={
                    "instrument_name": "CRO_USDC",
                    "side": "BUY",
                    "type": "LIMIT",
                    "price": 0.1233,
                    "quantity": 5,
                }
            )
        )
        event = await client.next_event()
        print(event)
        #
        await client.send(
            client.build_message(
                method="private/get-open-orders",
                params={
                    "instrument_name": "CRO_USDC",
                    "page_size": 10,
                    "page": 0
                }
            )
        )
        event = await client.next_event()
        print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

```
You can get all private methods in the [official documentation](https://exchange-docs.crypto.com/spot/index.html#websocket-subscriptions)