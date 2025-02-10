from typing import List, Union, Optional, Dict

from monday_async.types import QueryParams, ItemByColumnValuesParam, ColumnsMappingInput, ID
from monday_async.utils.queries.query_addons import add_complexity, add_updates, add_column_values, add_subitems
from monday_async.utils.utils import monday_json_stringify, format_param_value, graphql_parse, format_dict_value


def get_items_by_id_query(ids: Union[ID, List[ID]], newest_first: Optional[bool] = None,
                          exclude_nonactive: Optional[bool] = None, limit: int = 25, page: int = 1,
                          with_complexity: bool = False, with_column_values: bool = True,
                          with_subitems: bool = False, with_updates: bool = False) -> str:
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


def get_items_by_board_query(board_ids: Union[ID, List[ID]], query_params: Optional[QueryParams] = None,
                             limit: int = 25, cursor: str = None, with_complexity: bool = False,
                             with_column_values: bool = True, with_subitems: bool = False,
                             with_updates: bool = False) -> str:
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


def get_items_by_group_query(board_id: ID, group_id: ID, query_params: Optional[QueryParams] = None,
                             limit: int = 25, cursor: str = None, with_complexity: bool = False,
                             with_column_values: bool = True, with_subitems: bool = False,
                             with_updates: bool = False) -> str:
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


def get_items_by_column_value_query(board_id: ID, column_id: str, column_values: Union[str, List[str]], limit: int = 25,
                                    cursor: str = None, with_complexity: bool = False,
                                    with_column_values: bool = True, with_subitems: bool = False,
                                    with_updates: bool = False) -> str:
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


def get_items_by_multiple_column_values_query(board_id: ID, columns: Union[ItemByColumnValuesParam, dict, List[dict]],
                                              limit: int = 25, cursor: str = None, with_complexity: bool = False,
                                              with_column_values: bool = True, with_subitems: bool = False,
                                              with_updates: bool = False) -> str:
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


def next_items_page_query(cursor: str, limit: int = 500, with_complexity: bool = False, with_column_values: bool = True,
                          with_subitems: bool = False, with_updates: bool = False) -> str:
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


def create_item_query(item_name: str, board_id: ID, group_id: Optional[str] = None,
                      column_values: Optional[dict] = None, create_labels_if_missing: bool = False,
                      with_complexity: bool = False) -> str:
    """
    This query creates a new item on a specified board and group with a given name and optional column values.
    For more information, visit https://developer.monday.com/api-reference/reference/items#create-an-item

    Args:
        item_name (str): The name of the new item.

        board_id (ID): The ID of the board to create the item on.

        group_id (str): (Optional) The ID of the group to create the item in.

        column_values (dict): (Optional) The column values for the new item in JSON format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_item (
            item_name: {format_param_value(item_name)},
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def duplicate_item_query(board_id: ID, item_id: ID, with_updates: Optional[bool] = None,
                         with_complexity: bool = False) -> str:
    """
    This query creates a copy of an item on the same board, with the option to include updates.
    For more information, visit https://developer.monday.com/api-reference/reference/items#duplicate-an-item

    Args:
        board_id (ID): The ID of the board containing the item to duplicate.

        with_updates (bool): (Optional) Whether to include the item's updates in the duplication.

        item_id (ID): The ID of the item to duplicate.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        duplicate_item (
            board_id: {format_param_value(board_id)},
            with_updates: {format_param_value(with_updates)},
            item_id: {format_param_value(item_id)}
        ) {{
            id
            name
            column_values {{
                id
                text
                value
            }}
        }}
    }}
    """
    return graphql_parse(query)


def archive_item_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query archives an item, making it no longer visible in the active item list.
    For more information, visit https://developer.monday.com/api-reference/reference/items#archive-an-item
    Args:

        item_id (ID): The ID of the item to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def delete_item_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query permanently removes an item from a board.
    For more information, visit https://developer.monday.com/api-reference/reference/items#delete-an-item

    Args:
        item_id (ID): The ID of the item to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def get_subitems_by_parent_item_query(parent_item_id: ID, with_column_values: bool = True,
                                      with_complexity: bool = False) -> str:
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


def create_subitem_query(parent_item_id: ID, subitem_name: str, column_values: Optional[dict] = None,
                         create_labels_if_missing: bool = False, with_complexity: bool = False) -> str:
    """
    This query creates a new subitem under a specific parent item with a given name and optional column values.
    For more information, visit https://developer.monday.com/api-reference/reference/subitems#create-a-subitem

    Args:
        parent_item_id (ID): The ID of the parent item.

        subitem_name (str): The name of the new subitem.

        column_values (dict): (Optional) The column values for the new subitem in JSON format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_subitem (
            parent_item_id: {format_param_value(parent_item_id)},
            item_name: {format_param_value(subitem_name)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_multiple_item_column_values_query(item_id: ID, board_id: ID, column_values: dict,
                                             create_labels_if_missing: bool = False,
                                             with_complexity: bool = False) -> str:
    """
    This query updates the values of multiple columns for a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-multiple-column-values

    Args:
        item_id (ID): The ID of the item to update.

        board_id (ID): The ID of the board containing the item.

        column_values (dict): The updated column values as a dictionary in a {column_id: column_value, ...} format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_multiple_column_values (
            item_id: {format_param_value(item_id)},
            board_id: {format_param_value(board_id)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_item_column_json_value_query(item_id: ID, column_id: str, board_id: ID, value: dict,
                                        create_labels_if_missing: bool = False,
                                        with_complexity: bool = False) -> str:
    """
    This query updates the value of a specific column for an item using a JSON value. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-column-value

    Args:
        item_id (ID): (Optional) The ID of the item to update.

        column_id (str): The unique identifier of the column to update.

        board_id (ID): The ID of the board containing the item.

        value (dict): The new value for the column as a dictionary.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_value (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            board_id: {format_param_value(board_id)},
            value: {monday_json_stringify(value)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_item_column_simple_value_query(item_id: ID, column_id: str, board_id: ID, value: str,
                                          create_labels_if_missing: bool = False,
                                          with_complexity: bool = False) -> str:
    """
    This query updates the value of a specific column for an item using a simple string value.
    For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-simple-column-value

    Args:
        item_id (ID): (Optional) The ID of the item to update.

        column_id (str): The unique identifier of the column to update.

        board_id (ID): The ID of the board containing the item.

        value (str): The new simple string value for the column. Use null to clear the column value.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_simple_column_value (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            board_id: {format_param_value(board_id)},
            value: {format_param_value(value)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def upload_file_to_column_query(item_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This query uploads a file and adds it to a specific column of an item. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-file-to-the-file-column

    Args:
        item_id (ID): The ID of the item to add the file to.

        column_id (str): The unique identifier of the column to add the file to.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation ($file: File!){{{add_complexity() if with_complexity else ""}
        add_file_to_column (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            file: $file
        ) {{
            id
            name
            url
        }}
    }}
    """
    return graphql_parse(query)


def get_item_updates_query(item_id: ID, ids: Union[ID, List[ID]] = None,
                           limit: int = 25, page: int = 1, with_complexity: bool = False) -> str:
    """
    This query retrieves updates associated with a specific item, allowing pagination and filtering by update IDs.

    Args:
        item_id (ID): The ID of the item to retrieve updates from.

        ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.

        limit (int): (Optional) The maximum number of updates to return. Defaults to 25.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (ids: {format_param_value(item_id)}) {{
            updates (ids: {format_param_value(ids if ids else None)}, limit: {limit}, page: {page}) {{
                id
                text_body
                body
                creator_id
                assets {{
                    id 
                    name
                    file_extension
                    url
                    public_url 
                }}
                replies {{
                    id
                    text_body
                }}
                likes {{
                    id
                    reaction_type
                    creator_id
                    updated_at
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def clear_item_updates_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes all updates associated with a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/items#clear-an-items-updates

    Args:
        item_id (ID): The ID of the item to clear updates from.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        clear_item_updates (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def move_item_to_group_query(item_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This query moves an item to a different group within the same board. For more information, visit
    https://developer.monday.com/api-reference/reference/items#move-item-to-group

    Args:
        item_id (ID): The ID of the item to move.

        group_id (str): The ID of the target group within the board.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        move_item_to_group (
            item_id: {format_param_value(item_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
            name
            group {{
                id
                title
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


def move_item_to_board_query(board_id: ID, group_id: str, item_id: ID,
                             columns_mapping: Union[ColumnsMappingInput, List[Dict[str, str]]] = None,
                             subitems_columns_mapping: Union[ColumnsMappingInput, List[Dict[str, str]]] = None,
                             with_complexity=False) -> str:
    """
    This query moves an item to a different board. For more information, visit
    https://developer.monday.com/api-reference/reference/items#move-item-to-board

    Args:
        board_id (ID): The ID of the target board.
        group_id (str): The ID of the target group within the board.
        item_id (ID): The ID of the item to move.
        columns_mapping (Union[ColumnsMappingInput, List[Dict[str, str]]]): The object that defines the column mapping
            between the original and target board. Every column type can be mapped except for formula columns.
            If you omit this argument, the columns will be mapped based on the best match.
        subitems_columns_mapping (Union[ColumnsMappingInput, List[Dict[str, str]]]): The object that defines the
            subitems' column mapping between the original and target board.
            Every column type can be mapped except for formula columns.
            If you omit this argument, the columns will be mapped based on the best match.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.

    Raises:
        TypeError: If the columns_mapping or subitems_columns_mapping parameter is not a
        ColumnsMappingInput or a list of dictionaries.
    """

    def parse_mapping(mapping, name):
        if not mapping:
            return ""
        if isinstance(mapping, ColumnsMappingInput):
            return f"{name}: {mapping},"
        elif isinstance(mapping, list):
            formatted_list = ", ".join([format_dict_value(m) for m in mapping])
            return f"{name}: [{formatted_list}],"
        raise TypeError(f"Unsupported type for '{name}'. Expected ColumnsMappingInput or list of dictionaries.")

    columns_mapping_str = parse_mapping(columns_mapping, "columns_mapping")
    subitems_columns_mapping_str = parse_mapping(subitems_columns_mapping, "subitems_columns_mapping")
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        move_item_to_board (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            item_id: {format_param_value(item_id)},
            {columns_mapping_str}
            {subitems_columns_mapping_str}
        ) {{
            id
            name
            board {{
                id
                name
            }}
            group {{
                id
                title
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    "get_items_by_id_query",
    "get_items_by_board_query",
    "get_items_by_group_query",
    "get_items_by_column_value_query",
    "get_items_by_multiple_column_values_query",
    "next_items_page_query",
    "create_item_query",
    "duplicate_item_query",
    "archive_item_query",
    "delete_item_query",
    "get_subitems_by_parent_item_query",
    "create_subitem_query",
    "change_multiple_item_column_values_query",
    "change_item_column_json_value_query",
    "change_item_column_simple_value_query",
    "upload_file_to_column_query",
    "get_item_updates_query",
    "clear_item_updates_query",
    "move_item_to_group_query",
    "move_item_to_board_query"
]
