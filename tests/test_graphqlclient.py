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
from unittest.mock import AsyncMock, Mock, patch

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


@pytest.mark.asyncio
async def test_variables_sent_as_json_object_not_string():
    """
    Test that variables are sent as JSON objects, not JSON strings.
    This is required for API version 2025-04+ compliance.
    """
    client = AsyncGraphQLClient("https://api.monday.com/v2")
    client.inject_token("test_token")

    query = "query { boards { id } }"
    variables = {"board_id": 123, "name": "Test Board"}

    # Mock the response
    mock_response = Mock()
    mock_response.json = AsyncMock(return_value={"data": {"boards": [{"id": "123"}]}})

    # Mock the session.post context manager
    mock_post_cm = AsyncMock()
    mock_post_cm.__aenter__ = AsyncMock(return_value=mock_response)
    mock_post_cm.__aexit__ = AsyncMock(return_value=None)

    # Mock the session
    mock_session = Mock()
    mock_session.post = Mock(return_value=mock_post_cm)

    # Mock the ClientSession context manager
    mock_client_session_cm = AsyncMock()
    mock_client_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_client_session_cm.__aexit__ = AsyncMock(return_value=None)

    with patch("aiohttp.ClientSession", return_value=mock_client_session_cm):
        await client.execute(query, variables)

        # Verify the post method was called
        assert mock_session.post.called

        # Get the call arguments
        call_args = mock_session.post.call_args
        data_param = call_args.kwargs.get("data") or call_args.args[0] if call_args.args else None

        # Decode and parse the payload
        payload = json.loads(data_param.decode("utf-8"))

        # Verify that variables are a dict in the payload, not a JSON string
        assert "variables" in payload
        assert isinstance(payload["variables"], dict)
        assert payload["variables"] == variables
        assert payload["variables"]["board_id"] == 123
        assert payload["variables"]["name"] == "Test Board"
