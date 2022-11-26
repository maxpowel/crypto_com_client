Crypto.com websocket api client
=================================
[![Build Status](https://travis-ci.com/maxpowel/crypto_com_client.svg?branch=master)](https://travis-ci.com/maxpowel/crypto_com_client)
[![Maintainability](https://api.codeclimate.com/v1/badges/9c2c51fed72ca3aeacf6/maintainability)](https://codeclimate.com/github/maxpowel/crypto_com_client/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9c2c51fed72ca3aeacf6/test_coverage)](https://codeclimate.com/github/maxpowel/crypto_com_client/test_coverage)


This is a low level api client, it just connects the exchange api with your python code in the most simple way. Over
this library, you can build your awesome applications or high level api.
For more information, check the [library documentation](https://maxpowel.github.io/crypto_com_client/), the [official documentation](https://exchange-docs.crypto.com/) and the `examples` directory.

Features
--------
This library is optimized to be small, fast and secure. 
  * Fully tested: 100% code coverage
  * Simple: It just does one thing, but it does it right
  * Fast: Relies on asyncio so latency and memory usage is near zero (much better than threading or multiprocessing)
  * No forced dependencies: Just `websockets` and `orjson`. No super modern cool features that you probably don't want


Getting started
---------------
There are two kinds of `apis`, the `user` and `market`. 
The `user` type requires providing api credentials (access and secret key)

Before using the library, you have to install it:
```bash
pip install crypto_com_client
```

The most simple example, subscribing to an `orderbook`:

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

If you want to use the `user` api first get you api `key` and `secret`.

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
If you have any suggestion, detect any bug or want any feature, please open an `issue` so we can discuss it.


Tests
=====
To run the tests just run `tox`

It will run in first instance `flake8`, then `pylint` and finally `pytest` with code coverage check.
The only rule ignored is `max-line-length=120` basically because nowadays monitors are big enough for this.
Websockets import has E0611 disabled because pylint does not process `__all__` correctly