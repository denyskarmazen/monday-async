from typing import List, Union, Optional

from monday_async.types import ID
from monday_async.utils.queries.query_addons import add_complexity, add_updates
from monday_async.utils.utils import format_param_value, graphql_parse


def get_updates_query(ids: Optional[Union[ID, List[ID]]] = None, limit: int = 25, page: int = 1,
                      with_viewers: bool = False, with_complexity: bool = False) -> str:
    """
    This query retrieves updates, allowing pagination and filtering by update IDs. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#queries

    Args:
        ids (Union[ID, List[ID]]): A list of update IDs to retrieve specific updates.
        limit (int): the maximum number of updates to return. Defaults to 25. Maximum is 100 per page.
        page (int): The page number to return. Starts at 1.
        with_viewers (bool): Set to True to return the viewers of the update.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        {add_updates(ids=ids, limit=limit, page=page, with_viewers=with_viewers, with_pins=True, with_likes=True)}
    }}
    """
    return graphql_parse(query)


def create_update_query(body: str, item_id: ID, parent_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new update on a specific item or as a reply to another update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#create-an-update

    Args:
        body (str): The text content of the update as a string or in HTML format.
        item_id (ID): The ID of the item to create the update on.
        parent_id (Optional[ID]): The ID of the parent update to reply to.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_update (
            body: {format_param_value(body)},
            item_id: {format_param_value(item_id)},
            parent_id: {format_param_value(parent_id)}
        ) {{
            id
            body
            item_id
        }}
    }}
    """
    return graphql_parse(query)


def edit_update_query(update_id: ID, body: str, with_complexity: bool = False) -> str:
    """
    This query allows you to edit an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#edit-an-update

    Args:
        update_id (ID): The ID of the update to edit.
        body (str): The new text content of the update as a string or in HTML format.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        edit_update (
            id: {format_param_value(update_id)},
            body: {format_param_value(body)}
        ) {{
            id
            body
        }}
    }}
    """
    return graphql_parse(query)


def pin_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query pins an update to the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#pin-an-update
    Args:
        update_id (ID): The ID of the update to pin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        pin_to_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
            pinned_to_top {{
                item_id
            }}
        }}
    }}
    """
    return graphql_parse(query)


def unpin_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query unpins an update from the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unpin-an-update
    Args:
        update_id (ID): The ID of the update to unpin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unpin_from_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
            pinned_to_top {{
                item_id
            }}
        }}
    }}
    """
    return graphql_parse(query)


def like_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query adds a like to a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#like-an-update

    Args:
        update_id (ID): The ID of the update to like.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        like_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(query)


def unlike_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes a like from a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unlike-an-update

    Args:
        update_id (ID): The ID of the update to unlike.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unlike_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(query)


def delete_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#delete-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_update (id: {format_param_value(update_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def add_file_to_update(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query adds a file to an update. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-a-file-to-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """

    query = f"""
    mutation ($file: File!){{{add_complexity() if with_complexity else ""}
        add_file_to_update (update_id: {format_param_value(update_id)}, file: $file) {{
            id
            name
            url
            created_at
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    "get_updates_query",
    "create_update_query",
    "edit_update_query",
    "pin_update_query",
    "unpin_update_query",
    "like_update_query",
    "unlike_update_query",
    "delete_update_query",
    "add_file_to_update",
]
