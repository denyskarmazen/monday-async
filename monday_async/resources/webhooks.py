from monday_async.resources.base_resource import AsyncBaseResource
from typing import Union, Optional
from monday_async.utils.queries import get_webhooks_by_board_id_query, create_webhook_query, delete_webhook_query
from monday_async.utils.types import WebhookEventType


class WebhooksResource(AsyncBaseResource):
    async def get_webhooks_by_board_id(self, board_id: Union[int, str], with_complexity: bool = False):
        query = get_webhooks_by_board_id_query(board_id=board_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_webhook(self, board_id: Union[int, str], url: str, event: WebhookEventType, config: Optional[dict] = None,
                             with_complexity: bool = False):
        query = create_webhook_query(board_id=board_id, url=url, event=event, config=config,
                                     with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_webhook(self, webhook_id: Union[int, str], with_complexity: bool = False):
        query = delete_webhook_query(webhook_id=webhook_id, with_complexity=with_complexity)
        return await self.client.execute(query)
