import aiohttp
from typing import Optional
from monday_async.utils.graphqlclient import AsyncGraphQLClient


_URLS = {
    'prod': 'https://api.monday.com/v2',
    'file': 'https://api.monday.com/v2/file'
}


class AsyncBaseResource:
    def __init__(self, token: str, headers: dict, session: Optional[aiohttp.ClientSession] = None):
        self._token = token
        self.client = AsyncGraphQLClient(_URLS['prod'])
        self.file_upload_client = AsyncGraphQLClient(_URLS['file'])
        self.client.inject_token(token)
        self.client.inject_headers(headers)
        self.client.set_session(session)
        self.file_upload_client.inject_token(token)
        self.file_upload_client.inject_headers(headers)
        self.file_upload_client.set_session(session)

    async def _query(self, query: str):
        result = await self.client.execute(query=query)

        if result:
            return result

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
