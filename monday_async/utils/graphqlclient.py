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

import json
import os

import aiofiles
import aiohttp

from monday_async.exceptions import MondayAPIError
from monday_async.utils.response_parser import ResponseParser

TOKEN_HEADER = 'Authorization'


class AsyncGraphQLClient:
    """
    A client for interacting with a monday.com GraphQL API asynchronously.

    This client supports executing queries and mutations, including those requiring file uploads.

    Attributes:
        endpoint (str): The URL of the monday.com API endpoint.
        token (str, optional): The bearer token for authentication. Default is None.
        session (Optional[aiohttp.ClientSession]): Optional, externally managed aiohttp session. Recommended to use
                                                   the same session for all the requests.
                                                   If not provided, the client will create a new session for each
                                                   request which is not optimal.
        headers (dict): Additional headers to send with each request.
    """

    def __init__(self, endpoint: str):
        """
         Initializes a new instance of the GraphQLClient.

         Args:
             endpoint (str): The URL of the GraphQL endpoint.
         """
        self.endpoint = endpoint
        self.token = None
        self.session = None
        self.headers = {}

    async def execute(self, query: str, variables=None):
        """
        Executes a GraphQL query or mutation.

        Args:
            query (str): The GraphQL query or mutation.
            variables (dict, optional): A dictionary of variables for the query. Default is None.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        return await self._send(query, variables)

    def inject_token(self, token: str):
        """
        Injects an authentication token to be used for all requests.

        Args:
            token (str): The bearer token for authentication.
        """
        self.token = token

    def inject_headers(self, headers: dict):
        """
        Injects additional headers to be used for all requests.

        Args:
            headers (dict): A dictionary of headers to add to the request.
        """
        self.headers = headers

    def set_session(self, session: aiohttp.ClientSession):
        """
        Sets an external aiohttp.ClientSession to be used by the client.

        This allows for external management of the session's lifecycle.

        Args:
            session (aiohttp.ClientSession): An externally managed aiohttp session.
        """
        self.session = session

    async def close_session(self):
        """
        Closes the aiohttp.ClientSession if it was set externally and is no longer needed.

        Important: This method is intended for use cases where the GraphQLClient is
        responsible for session lifecycle management.
        It should be used with caution, as closing a session that's shared or
        managed externally can lead to unexpected behavior.
        """
        if self.session:
            await self.session.close()
            self.session = None

    async def _send(self, query: str, variables):
        """
        Sends the GraphQL query or mutation to the server.

        This method constructs the appropriate HTTP request based on the presence of variables
        and/or files and handles the response.

        Args:
            query (str): The GraphQL query or mutation.
            variables (dict, optional): A dictionary of variables for the query.

        Returns:
            dict: The JSON response from the GraphQL server.

        Raises:
            MondayQueryError: If the GraphQL server returns errors.
        """
        headers = self.headers.copy()

        if self.token is not None:
            headers[TOKEN_HEADER] = self.token

        if variables is None:
            headers.setdefault('Content-Type', 'application/json')

            payload = json.dumps({'query': query}).encode('utf-8')

        else:
            if 'file' in variables:
                filename = os.path.basename(variables['file'])
                map_data = '{"0": ["variables.file"]}'

                data = aiohttp.FormData()
                data.add_field('query', query)
                data.add_field('map', map_data)

                async with aiofiles.open(variables['file'], 'rb') as file:
                    file_content = await file.read()
                    data.add_field('0', file_content, filename=filename, content_type='application/octet-stream')

                payload = data
            else:
                headers.setdefault('Content-Type', 'application/json')

                payload = json.dumps({'query': query, 'variables': variables}).encode('utf-8')

        if not self.session:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.endpoint, headers=headers, data=payload) as response:
                        response_data = await response.json()
                        parser = ResponseParser(response_data, query)
                        data = parser.parse_response()
                        return data
            except (aiohttp.ClientError, json.JSONDecodeError, MondayAPIError) as e:
                if self.session:
                    await self.close_session()
                raise e
        else:
            async with self.session.post(self.endpoint, headers=headers, data=payload) as response:
                response_data = await response.json()
                parser = ResponseParser(response_data, query)
                data = parser.parse_response()
                return data
