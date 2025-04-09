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

from typing import Optional

from aiohttp import ClientSession

from monday_async import __version__
from monday_async.resources import (
    APIResource, CustomResource, WebhooksResource, NotificationResource, UsersResource, WorkspaceResource,
    FolderResource, BoardResource, TagResource, ColumnResource, GroupResource, ItemResource, UpdateResource,
    ComplexityResource, AccountResource, TeamsResource
)

_DEFAULT_HEADERS = {
    "API-Version": "2025-01"
}


class AsyncMondayClient:
    """
    Attributes:
        complexity (ComplexityResource):
        custom (CustomResource):
        api (APIResource):
        account (AccountResource):
        webhooks (WebhooksResource):
        notifications (NotificationResource):
        users (UsersResource):
        teams (TeamsResource):
        workspaces (WorkspaceResource):
        folders (FolderResource):
        boards (BoardResource):
        tags (TagResource):
        columns (ColumnResource):
        groups (GroupResource):
        items (ItemResource):
        updates (UpdateResource):
    """

    def __init__(self, token: str, session: Optional[ClientSession] = None, headers: dict = None):
        """
        Args:
            token (str): Your monday.com API access token.
            session (ClientSession): Optional, externally managed aiohttp session. Recommended to use the same session
                for all the requests.
            headers (dict): Additional headers to send with each request.
        """
        self._session = session
        self._external_session = True if session else False

        if not headers:
            headers = _DEFAULT_HEADERS.copy()

        self.complexity = ComplexityResource(token=token, headers=headers, session=self._session)
        self.custom = CustomResource(token=token, headers=headers, session=self._session)
        self.api = APIResource(token=token, headers=headers, session=self._session)
        self.account = AccountResource(token=token, headers=headers, session=self._session)
        self.webhooks = WebhooksResource(token=token, headers=headers, session=self._session)
        self.notifications = NotificationResource(token=token, headers=headers, session=self._session)
        self.users = UsersResource(token=token, headers=headers, session=self._session)
        self.teams = TeamsResource(token=token, headers=headers, session=self._session)
        self.workspaces = WorkspaceResource(token=token, headers=headers, session=self._session)
        self.folders = FolderResource(token=token, headers=headers, session=self._session)
        self.boards = BoardResource(token=token, headers=headers, session=self._session)
        self.tags = TagResource(token=token, headers=headers, session=self._session)
        self.columns = ColumnResource(token=token, headers=headers, session=self._session)
        self.groups = GroupResource(token=token, headers=headers, session=self._session)
        self.items = ItemResource(token=token, headers=headers, session=self._session)
        self.updates = UpdateResource(token=token, headers=headers, session=self._session)

    def __enter__(self):
        raise RuntimeError('Use `async with AsyncMondayClient(...)` instead of `with AsyncMondayClient(...)`')

    def __exit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        if not self._session:
            self._session = ClientSession()
            self._external_session = False
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if not self._external_session and self._session:
            await self._session.close()

    def __str__(self):
        return f'AsyncMondayClient {__version__}'

    def __repr__(self):
        return f'AsyncMondayClient {__version__}'
