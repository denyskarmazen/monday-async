# monday_adsync
An asynchronous Python client library for monday.com

Check out monday.com api [here](https://developer.monday.com/api-reference/).

#### Usage Example
```python
import asyncio
from monday_async import AsyncMondayClient
from aiohttp import ClientSession

async def main():
    # Can be used without providing a session
    # But recommended to use the same session for all requests
    session = ClientSession()
    client = AsyncMondayClient(token="YOUR_API_KEY", session=session)
    
    await client.users.get_me()
    
    await session.close()

asyncio.run(main())
```