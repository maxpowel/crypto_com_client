Crypto.com websocket api client
=================================

This is a low level api client, it just connects the exchange api with your python code in the most simple way.
Check the official documentation https://exchange-docs.crypto.com/ and the examples directory.

Getting started
---------------
There two kinds of `apis`, the `user` and `market`. You can specify which one to use by using the `client_type`. The 
`user` type requires to create api credentials (access and secret key)

Before use the library, you have to install it:
```bash
pip install crypto_com
```

The most simple example, subscribing to an `orderbook`:

```python
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

```

If you want to use the `user` api you can use the following example. The differences are the `client_type` and the `access_key`
and `secret_key`

```python
from crypto_com import CryptoClient
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

async def run():
    async with CryptoClient(
            client_type=CryptoClient.USER,
            api_key=os.environ["API_KEY"],
            api_secret=os.environ["API_SECRET"]
    ) as client:
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

With these two examples you can use the whole api. Just check the API documentation to know the different methods
and parameters.

Contributing
============
If you have any suggestion, detect any bug or want any feature, please open an `issue` so we can discuss about it.