from typing import Union, Optional

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import WebhookEventType
from monday_async.utils.queries import get_webhooks_by_board_id_query, create_webhook_query, delete_webhook_query


class WebhooksResource(AsyncBaseResource):
    async def get_webhooks_by_board_id(self, board_id: Union[int, str], app_webhooks_only: bool = False,
                                       with_complexity: bool = False) -> dict:
        """
        Get all webhooks for a board. For more information, visit
        https://developer.monday.com/api-reference/reference/webhooks#queries

        Args:
            board_id (Union[int, str]): a unique identifier of a board, can be an integer or a string containing
                integers.
            app_webhooks_only (bool): if set to Trues returns only the webhooks created by
                the app initiating the request.
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = get_webhooks_by_board_id_query(board_id=board_id, app_webhooks_only=app_webhooks_only,
                                               with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_webhook(self, board_id: Union[int, str], url: str, event: WebhookEventType,
                             config: Optional[dict] = None, with_complexity: bool = False) -> dict:
        """
        Create a webhook. For more information, visit
        https://developer.monday.com/api-reference/reference/webhooks#create-a-webhook

        Args:
            board_id (Union[int, str]): a unique identifier of a board, can be an integer or
                                        a string containing integers.
            url (str): the webhook URL.
            event (WebhookEventType): the event type to listen to.
            config (dict): the webhook configuration,
                check https://developer.monday.com/api-reference/reference/webhooks
            for more info.
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = create_webhook_query(board_id=board_id, url=url, event=event, config=config,
                                     with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_webhook(self, webhook_id: Union[int, str], with_complexity: bool = False) -> dict:
        """
        Delete a webhook connection. For more information, visit
        https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

        Args:
            webhook_id (Union[int, str]): a unique identifier of a webhook, can be an integer or
                                        a string containing integers.
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """

        query = delete_webhook_query(webhook_id=webhook_id, with_complexity=with_complexity)
        return await self.client.execute(query)
