# Market Client

You can use this client to perform private actions. You can get you balance, the status of your orders, create or 
cancel orders...

In this example we are subscribing to the `CRO` order book

```python
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

```
You can get all public methods in the [official documentation](https://exchange-docs.crypto.com/spot/index.html#websocket-subscriptions)