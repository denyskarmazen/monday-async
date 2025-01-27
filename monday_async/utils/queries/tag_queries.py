from typing import List, Union, Optional

from monday_async.types import ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def get_tags_query(ids: Union[ID, List[ID]] = None, with_complexity: bool = False) -> str:
    """
    This query retrieves tags, allowing you to specify individual tags or retrieve all tags. For more information, visit
    https://developer.monday.com/api-reference/reference/tags-1#queries

    Args:
        ids (Union[ID, List[ID]]): (Optional) A list of tag IDs to retrieve specific tags.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        tags (ids: {format_param_value(ids if ids else None)}) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


def get_tags_by_board_query(board_id: ID, with_complexity: bool = False) -> str:
    """
    This query retrieves tags associated with a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/tags-1#queries

    Args:
        board_id (ID): The ID of the board to retrieve tags from.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            tags {{
                id
                name
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_or_get_tag_query(tag_name: str, board_id: Optional[ID] = None,
                            with_complexity: bool = False) -> str:
    """
    This query creates a new tag with the specified name or retrieves the existing tag if it already exists.
    For more information, visit https://developer.monday.com/api-reference/reference/tags-1#create-or-get-a-tag

    Args:
        tag_name (str): The name of the tag to create or retrieve.

        board_id (ID): (Optional) The ID of the private board to create the tag in. Not needed for public boards.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_or_get_tag (
            tag_name: {format_param_value(tag_name)},
            board_id: {format_param_value(board_id)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_tags_query',
    'get_tags_by_board_query',
    'create_or_get_tag_query'
]