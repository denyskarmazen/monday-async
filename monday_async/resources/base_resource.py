# monday-async
# Copyright 2025 Denys Karmazeniuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import aiohttp

from monday_async.core.client import AsyncGraphQLClient

_URLS = {"prod": "https://api.monday.com/v2", "file": "https://api.monday.com/v2/file"}


class AsyncBaseResource:
    def __init__(self, token: str, headers: dict, session: aiohttp.ClientSession | None = None):
        self._token = token
        self.client = AsyncGraphQLClient(_URLS["prod"])
        self.file_upload_client = AsyncGraphQLClient(_URLS["file"])
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
