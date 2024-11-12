from typing import Optional

from aiohttp import ClientSession

from ._version import __version__
from .resources import (
    APIResource, CustomResource, WebhooksResource, NotificationResource, UsersResource, WorkspaceResource,
    FolderResource, BoardResource, TagResource, ColumnResource, GroupResource, ItemResource, UpdateResource,
    ComplexityResource, AccountResource
)

_DEFAULT_HEADERS = {
    "API-Version": "2024-10"
}


class AsyncMondayClient:
    """
    Attributes:
        complexity (ComplexityResource):
        custom (CustomResource):
        api (APIResource):
        webhooks (WebhooksResource):
        notifications (NotificationResource):
        users (UsersResource):
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

        if not headers:
            headers = _DEFAULT_HEADERS.copy()

        self.complexity = ComplexityResource(token=token, headers=headers, session=session)
        self.custom = CustomResource(token=token, headers=headers, session=session)
        self.api = APIResource(token=token, headers=headers, session=session)
        self.account = AccountResource(token=token, headers=headers, session=session)
        self.webhooks = WebhooksResource(token=token, headers=headers, session=session)
        self.notifications = NotificationResource(token=token, headers=headers, session=session)
        self.users = UsersResource(token=token, headers=headers, session=session)
        self.workspaces = WorkspaceResource(token=token, headers=headers, session=session)
        self.folders = FolderResource(token=token, headers=headers, session=session)
        self.boards = BoardResource(token=token, headers=headers, session=session)
        self.tags = TagResource(token=token, headers=headers, session=session)
        self.columns = ColumnResource(token=token, headers=headers, session=session)
        self.groups = GroupResource(token=token, headers=headers, session=session)
        self.items = ItemResource(token=token, headers=headers, session=session)
        self.updates = UpdateResource(token=token, headers=headers, session=session)

    def __str__(self):
        return f'AsyncMondayClient {__version__}'

    def __repr__(self):
        return f'AsyncMondayClient {__version__}'
