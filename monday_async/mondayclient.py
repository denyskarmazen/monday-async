from aiohttp import ClientSession
from monday_async._version import __version__
from monday_async.resources import (
    APIResource, CustomResource, WebhooksResource, NotificationResource, UsersResource, WorkspaceResource,
    FolderResource, BoardResource, TagResource
)


_DEFAULT_HEADERS = {
    "API-Version": "2024-04"
}


class AsyncMondayClient:
    def __init__(self, token: str, session: ClientSession = None, headers=None):
        """
        :param token:
        :param session:
        :param headers:
        """

        if not headers:
            headers = _DEFAULT_HEADERS.copy()

        self.custom = CustomResource(token=token, headers=headers, session=session)
        self.api = APIResource(token=token, headers=headers, session=session)
        self.webhooks = WebhooksResource(token=token, headers=headers, session=session)
        self.notifications = NotificationResource(token=token, headers=headers, session=session)
        self.users = UsersResource(token=token, headers=headers, session=session)
        self.workspaces = WorkspaceResource(token=token, headers=headers, session=session)
        self.folders = FolderResource(token=token, headers=headers, session=session)
        self.boards = BoardResource(token=token, headers=headers, session=session)
        self.tags = TagResource(token=token, headers=headers, session=session)


    def __str__(self):
        return f'AsyncMondayClient {__version__}'

    def __repr__(self):
        return f'AsyncMondayClient {__version__}'
