from typing import Union, Optional

from monday_async.types import WebhookEventType, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import monday_json_stringify, format_param_value, graphql_parse


def get_webhooks_by_board_id_query(board_id: ID, app_webhooks_only: bool = False, with_complexity: bool = False) -> str:
    """
    Construct a query to get all webhooks for a board. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#queries

    Args:
        board_id (Union[int, str]): a unique identifier of a board, can be an integer or
            a string containing integers.
        app_webhooks_only (bool): if set to Trues returns only the webhooks created by the app initiating the request.
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        webhooks(
            app_webhooks_only: {format_param_value(app_webhooks_only)}, 
            board_id: {format_param_value(board_id)}
        ) {{
            id
            event
            board_id
            config
        }}
    }}
    """
    return graphql_parse(query)


def create_webhook_query(board_id: ID, url: str, event: WebhookEventType, config: Optional[dict] = None,
                         with_complexity: bool = False) -> str:
    """
    Construct a query to create a webhook. For more information, visit
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
    query = f"""
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
    return graphql_parse(query)


def delete_webhook_query(webhook_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to delete a webhook connection. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

    Args:
        webhook_id (ID): a unique identifier of a webhook, can be an integer or
            a string containing integers.

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_webhook (id: {format_param_value(webhook_id)}) {{
            id
            board_id
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_webhooks_by_board_id_query',
    'create_webhook_query',
    'delete_webhook_query'
]
