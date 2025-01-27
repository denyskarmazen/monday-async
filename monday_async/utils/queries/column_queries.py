from typing import List, Union, Optional

from monday_async.types import ColumnType, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import monday_json_stringify, format_param_value, graphql_parse


def get_columns_by_board_query(board_id: ID, ids: Union[ID, List[ID]] = None,
                               types: Union[ColumnType, List[ColumnType]] = None, with_complexity: bool = False) -> str:
    """
    This query retrieves columns associated with a specific board, allowing filtering by column IDs and types.
    For more information, visit https://developer.monday.com/api-reference/reference/columns#queries

    Args:
        board_id (ID): The ID of the board to retrieve columns from.

        ids (Union[ID, List[ID]]): (Optional) A list of column IDs to retrieve specific columns.

        types (List[ColumnType]): (Optional) A list of column types to filter by.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            id
            name
            columns (ids: {format_param_value(ids if ids else None)}, types: {format_param_value(types)}) {{
                id
                title
                type
                description
                settings_str
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_column_query(board_id: ID, title: str, column_type: ColumnType, description: Optional[str] = None,
                        defaults: Optional[dict] = None, column_id: Optional[str] = None,
                        after_column_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new column on a specific board with a specified title, type, and optional description,
    defaults, user-specified ID, and positioning.
    For more information, visit https://developer.monday.com/api-reference/reference/columns#create-a-column

    Args:
        board_id (ID): The ID of the board to create the column on.

        title (str): The title of the new column.

        column_type (ColumnType): The type of column to create, chosen from the ColumnType enum.

        description (str): (Optional) A description for the new column.

        defaults (dict): (Optional) The default value for the new column as a dictionary.

        column_id (str): (Optional) A user-specified unique identifier for the column. Has to meet requirements:
            - [1-20] characters in length (inclusive)
            - Only lowercase letters (a-z) and underscores (_)
            - Must be unique (no other column on the board can have the same ID)
            - Can't reuse column IDs, even if the column has been deleted from the board
            - Can't be null, blank, or an empty string

        after_column_id (ID): (Optional) The ID of the column after which to insert the new column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    column_type_value = column_type.value if isinstance(column_type, ColumnType) else column_type
    id_value = f"id: {format_param_value(column_id)}" if column_id else ""
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_column (
            board_id: {format_param_value(board_id)},
            title: {format_param_value(title)},
            column_type: {column_type_value},
            description: {format_param_value(description)},
            defaults: {monday_json_stringify(defaults)},
            after_column_id: {format_param_value(after_column_id)},
            {id_value}
        ) {{
            id
            title
            type
            description
        }}
    }}
    """
    return graphql_parse(query)


def change_column_title_query(board_id: ID, column_id: str, title: str,
                              with_complexity: bool = False) -> str:
    """
    This query updates the title of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-column-title

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        title (str): The new title for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_title (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)},
            title: {format_param_value(title)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(query)


def change_column_description_query(board_id: ID, column_id: str, description: str,
                                    with_complexity: bool = False) -> str:
    """
    This query updates the description of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-column-metadata

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        description (str): The new description for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_metadata (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)},
            column_property: description,
            value: {format_param_value(description)}
        ) {{
            id
            title
            description
        }}
    }}
    """
    return graphql_parse(query)


def delete_column_query(board_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This query removes a column from a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#delete-a-column

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_column (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_columns_by_board_query',
    'create_column_query',
    'change_column_title_query',
    'change_column_description_query',
    'delete_column_query'
]