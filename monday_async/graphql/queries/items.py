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


from typing import Optional

from monday_async.core.helpers import format_dict_value, format_param_value, graphql_parse
from monday_async.graphql.addons import add_column_values, add_complexity, add_subitems, add_updates
from monday_async.types import ID, ItemByColumnValuesParam, QueryParams


def get_items_by_id_query(
    ids: ID | list[ID],
    newest_first: bool | None = None,
    exclude_nonactive: bool | None = None,
    limit: int = 25,
    page: int = 1,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query retrieves items, allowing filtering by IDs, sorting, and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items#queries

    Args:
        ids (Union[ID, List[ID]]):  A list of item IDs to retrieve specific items.

        newest_first (bool): (Optional) Set to True to order results with the most recently created items first.

        exclude_nonactive (bool): (Optional) Set to True to exclude inactive, deleted,
            or items belonging to deleted items.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (
            ids: {format_param_value(ids)},
            newest_first: {format_param_value(newest_first)},
            exclude_nonactive: {format_param_value(exclude_nonactive)},
            limit: {limit},
            page: {page}
        ) {{
            id
            name
            state
            {add_updates() if with_updates else ""}
            {add_column_values() if with_column_values else ""}
            {add_subitems() if with_subitems else ""}
            url
            group {{
                id
                title
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_board_query(
    board_ids: ID | list[ID],
    query_params: QueryParams | None = None,
    limit: int = 25,
    cursor: Optional[str] = None,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query retrieves items from a specific board, allowing filtering by IDs, sorting, and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

    Args:
        board_ids (ID): The ID of the board to retrieve items from.

        query_params (QueryParams): (Optional) A set of parameters to filter, sort,
            and control the scope of the boards query. Use this to customize the results based on specific criteria.
            Please note that you can't use query_params and cursor in the same request.
            We recommend using query_params for the initial request and cursor for paginated requests.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    # If a cursor is provided setting query_params to None
    # since you cant use query_params and cursor in the same request.
    if cursor:
        query_params = None

    if query_params:
        query_params_value = f"query_params: {query_params}"
    else:
        query_params_value = ""

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_ids)}) {{
            items_page (
                limit: {limit},
                cursor: {format_param_value(cursor)},
                {query_params_value},
            ) {{
                cursor
                items {{
                    id
                    name
                    state
                    {add_updates() if with_updates else ""}
                    {add_column_values() if with_column_values else ""}
                    {add_subitems() if with_subitems else ""}
                    url
                    group {{
                        id
                        title
                        color
                    }}
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_group_query(
    board_id: ID,
    group_id: ID,
    query_params: QueryParams | None = None,
    limit: int = 25,
    cursor: Optional[str] = None,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query retrieves items from a specific group within a board, allowing filtering by IDs, sorting,
    and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

    Args:
        board_id (ID): The ID of the board to retrieve items from.

        group_id (ID): The ID of the group to get the items by

        query_params (QueryParams): (Optional) A set of parameters to filter, sort,
            and control the scope of the boards query. Use this to customize the results based on specific criteria.
            Please note that you can't use query_params and cursor in the same request.
            We recommend using query_params for the initial request and cursor for paginated requests.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    # If a cursor is provided setting query_params to None
    # since you cant use query_params and cursor in the same request.
    if cursor:
        query_params = None

    if query_params:
        query_params_value = f"query_params: {query_params}"
    else:
        query_params_value = ""

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            groups (ids: {format_param_value(group_id)}) {{
                items_page (
                    limit: {limit},
                    cursor: {format_param_value(cursor)},
                    {query_params_value},
                ) {{
                    cursor
                    items {{
                        id
                        name
                        state
                        {add_updates() if with_updates else ""}
                        {add_column_values() if with_column_values else ""}
                        {add_subitems() if with_subitems else ""}
                        url
                    }}
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_column_value_query(
    board_id: ID,
    column_id: str,
    column_values: str | list[str],
    limit: int = 25,
    cursor: Optional[str] = None,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query retrieves items based on the value of a specific column. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

    Args:
        board_id (ID): The ID of the board containing the items.

        column_id (str): The unique identifier of the column to filter by.

        column_values (Union[str, List[str]]): The column value to search for.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    if cursor:
        columns_value = ""

    else:
        params = ItemByColumnValuesParam()
        params.add_column(column_id=column_id, column_values=column_values)
        columns_value = f"columns: {params}"

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items_page_by_column_values (
            board_id: {format_param_value(board_id)},
            limit: {limit},
            cursor: {format_param_value(cursor)},
            {columns_value}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_multiple_column_values_query(
    board_id: ID,
    columns: ItemByColumnValuesParam | dict | list[dict],
    limit: int = 25,
    cursor: Optional[str] = None,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query retrieves items based on the value of a specific column. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

    Args:
        board_id (ID): The ID of the board containing the items.

        columns (Union[ItemByColumnValuesParam, dict]): The column values to filter by can be ItemByColumnValuesParam
            instance or a list consisting of dictionaries of this format:
            {"column_id": column_id, "column_values": column_values}

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    if cursor:
        columns_value = ""

    else:
        if isinstance(columns, ItemByColumnValuesParam):
            columns_value = f"columns: {columns}"

        elif isinstance(columns, list):
            formatted_columns = f"[{', '.join(format_dict_value(column) for column in columns)}]"
            columns_value = f"columns: {formatted_columns}"

        elif isinstance(columns, dict):
            columns_value = f"columns: [{format_dict_value(columns)}]"

        else:
            raise TypeError(
                "Unsupported type for 'columns' parameter. Expected ItemByColumnValuesParam, dict, "
                "or list of dictionaries. For more information visit \n"
                "https://developer.monday.com/api-reference/reference/other-types#items-page-by-column-values-query"
            )

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items_page_by_column_values (
            board_id: {format_param_value(board_id)},
            limit: {limit},
            cursor: {format_param_value(cursor)},
            {columns_value}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def next_items_page_query(
    cursor: str,
    limit: int = 500,
    with_complexity: bool = False,
    with_column_values: bool = True,
    with_subitems: bool = False,
    with_updates: bool = False,
) -> str:
    """
    This query returns the next set of items that correspond with the provided cursor. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page#cursor-based-pagination-using-next_items_page

    Args:
        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        limit (int): The number of items to return. 500 by default, the maximum is 500.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        next_items_page (
            cursor: {format_param_value(cursor)},
            limit: {limit}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_subitems_by_parent_item_query(
    parent_item_id: ID, with_column_values: bool = True, with_complexity: bool = False
) -> str:
    """
    This query retrieves subitems of a specific item.
    For more information, visit https://developer.monday.com/api-reference/reference/subitems#queries

    Args:
        parent_item_id (ID): The ID of the parent item to retrieve subitems from.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (ids: {format_param_value(parent_item_id)}) {{
            subitems {{
                id
                name
                state
                {add_column_values() if with_column_values else ""}
                url
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_item_updates_query(
    item_id: ID,
    ids: ID | list[ID] = None,
    limit: int = 25,
    page: int = 1,
    with_viewers: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This query retrieves updates associated with a specific item, allowing pagination and filtering by update IDs.

    Args:
        item_id (ID): The ID of the item to retrieve updates from.
        ids (Union[ID, List[ID]]): A list of update IDs to retrieve specific updates.
        limit (int): The maximum number of updates to return. Defaults to 25.
        page (int): The page number to return. Starts at 1.
        with_viewers (bool): Set to True to return the viewers of the update.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (ids: {format_param_value(item_id)}) {{
            {add_updates(ids=ids, limit=limit, page=page, with_viewers=with_viewers, with_pins=True, with_likes=True)}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    "get_item_updates_query",
    "get_items_by_board_query",
    "get_items_by_column_value_query",
    "get_items_by_group_query",
    "get_items_by_id_query",
    "get_items_by_multiple_column_values_query",
    "get_subitems_by_parent_item_query",
    "next_items_page_query",
]
