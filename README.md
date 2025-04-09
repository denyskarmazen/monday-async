# monday-async &middot; [![Tests](https://github.com/denyskarmazen/monday-async/actions/workflows/project-tests.yml/badge.svg)](https://github.com/denyskarmazen/monday-async/actions/workflows/project-tests.yml)

An asynchronous Python client library for monday.com

Check out monday.com API [here](https://developer.monday.com/api-reference/).

### Install
#### Python Requirements:
- Python >= 3.9

To install the latest version run:
```bash
pip install monday-async
```

### Example

```python
import asyncio

from monday_async import AsyncMondayClient


async def main():
    with AsyncMondayClient(token="YOUR_API_KEY") as client:
        boards = await client.boards.get_boards()


asyncio.run(main())
```

### License
This project is licensed under the [Apache-2.0 license](LICENSE).
