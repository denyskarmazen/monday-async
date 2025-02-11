# monday_async | [![Tests](https://github.com/JUSTFUN0368/monday-async/actions/workflows/project-tests.yml/badge.svg?branch=main)](https://github.com/JUSTFUN0368/monday-async/actions/workflows/project-tests.yml)

An asynchronous Python client library for monday.com

Check out monday.com api [here](https://developer.monday.com/api-reference/).

#### Usage Example
```python
import asyncio
from monday_async import AsyncMondayClient
from aiohttp import ClientSession

async def main():
    with ClientSession() as session:
        client = AsyncMondayClient(token="YOUR_API_KEY", session=session)
        boards = await client.boards.get_boards()
        
asyncio.run(main())
```