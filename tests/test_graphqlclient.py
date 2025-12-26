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

import pytest
from aiohttp import ClientSession

from monday_async.core.client import AsyncGraphQLClient


@pytest.fixture(scope="session")
def graphql_clients():
    """Fixture to create instances of AsyncGraphQLClient and common test data."""
    endpoint = "https://api.monday.com/v2"
    file_endpoint = "https://api.monday.com/v2/file"
    token = "abcd123"
    headers = {"API-Version": "2025-01"}

    graph_ql_client = AsyncGraphQLClient(endpoint)
    file_graph_ql_client = AsyncGraphQLClient(file_endpoint)

    # Return all items needed by multiple tests
    return {
        "graph_ql_client": graph_ql_client,
        "file_graph_ql_client": file_graph_ql_client,
        "token": token,
        "headers": headers,
    }


def test_token_injection(graphql_clients):
    """Test that token injection correctly updates the client's token."""
    client = graphql_clients["graph_ql_client"]
    token = graphql_clients["token"]

    client.inject_token(token)
    assert client.token == token

    new_token = "efgh456"
    client.inject_token(new_token)
    assert client.token == new_token


def test_headers_injection(graphql_clients):
    """Test that headers injection correctly updates the client's headers."""
    client = graphql_clients["graph_ql_client"]
    headers = graphql_clients["headers"]

    client.inject_headers(headers)
    assert client.headers == headers

    new_headers = {"API-Version": "2024-10"}
    client.inject_headers(new_headers)
    assert client.headers == new_headers


@pytest.mark.asyncio
async def test_session_setting(graphql_clients):
    client = graphql_clients["graph_ql_client"]
    assert client.session is None

    async with ClientSession() as session:
        client.set_session(session)
        assert client.session == session


@pytest.mark.asyncio
async def test_close_session(graphql_clients):
    client = graphql_clients["graph_ql_client"]
    if not client.session:
        async with ClientSession() as session:
            client.set_session(session)

    await client.close_session()
    assert client.session is None
