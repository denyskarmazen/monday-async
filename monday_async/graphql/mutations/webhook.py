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


from monday_async.core.helpers import format_param_value, graphql_parse, monday_json_stringify
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, WebhookEventType


def create_webhook_mutation(
    board_id: ID, url: str, event: WebhookEventType, config: dict | None = None, with_complexity: bool = False
) -> str:
    """
    Construct a mutation to create a webhook. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#create-a-webhook

    Args:
        board_id (ID): a unique identifier of a board, can be an integer or a string containing integers.
        url (str): the webhook URL.
        event (WebhookEventType): the event type to listen to.
        config (dict): the webhook configuration, check https://developer.monday.com/api-reference/reference/webhooks
            for more info.
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    event_value = event.value if isinstance(event, WebhookEventType) else event
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_webhook (
            board_id: {format_param_value(board_id)},
            url: {format_param_value(url)},
            event: {event_value},
            config: {monday_json_stringify(config)}
        ) {{
            id
            board_id
            event
            config
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_webhook_mutation(webhook_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a mutation to delete a webhook connection. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

    Args:
        webhook_id (ID): a unique identifier of a webhook, can be an integer or
            a string containing integers.

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_webhook (id: {format_param_value(webhook_id)}) {{
            id
            board_id
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = ["create_webhook_mutation", "delete_webhook_mutation"]
