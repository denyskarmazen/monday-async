# monday-async &middot; [![Tests](https://github.com/denyskarmazen/monday-async/actions/workflows/project-tests.yml/badge.svg)](https://github.com/denyskarmazen/monday-async/actions/workflows/project-tests.yml) [![PyPI Downloads](https://static.pepy.tech/badge/monday-async)](https://pepy.tech/projects/monday-async) [![Monday.com API Version](https://img.shields.io/badge/Monday_API_Version-2025--04-green)](https://developer.monday.com/api-reference/docs/release-notes#2025-04)
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
    async with AsyncMondayClient(token="YOUR_API_KEY") as client:
        boards = await client.boards.get_boards()


asyncio.run(main())
```

### Changelog
See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

### License
This project is licensed under the [Apache-2.0 license](LICENSE).
