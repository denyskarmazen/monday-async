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


from monday_async.graphql.mutations import create_webhook_mutation, delete_webhook_mutation
from monday_async.graphql.queries import get_webhooks_by_board_id_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import WebhookEventType


class WebhooksResource(AsyncBaseResource):
    async def get_webhooks_by_board_id(
        self, board_id: int | str, app_webhooks_only: bool = False, with_complexity: bool = False
    ) -> dict:
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
        query = get_webhooks_by_board_id_query(
            board_id=board_id, app_webhooks_only=app_webhooks_only, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def create_webhook(
        self,
        board_id: int | str,
        url: str,
        event: WebhookEventType,
        config: dict | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a webhook. For more information, visit
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
        mutation = create_webhook_mutation(
            board_id=board_id, url=url, event=event, config=config, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def delete_webhook(self, webhook_id: int | str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to delete a webhook connection. For more information, visit
        https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

        Args:
            webhook_id (Union[int, str]): a unique identifier of a webhook, can be an integer or
                                        a string containing integers.
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """

        mutation = delete_webhook_mutation(webhook_id=webhook_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)
