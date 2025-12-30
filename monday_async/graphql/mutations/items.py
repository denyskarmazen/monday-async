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


from monday_async.core.helpers import format_dict_value, format_param_value, graphql_parse, monday_json_stringify
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, ColumnsMappingInput


def create_item_mutation(
    item_name: str,
    board_id: ID,
    group_id: str | None = None,
    column_values: dict | None = None,
    create_labels_if_missing: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a new item on a specified board and group with a given name and optional column values.
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
    # FIXME make sure the item name is in one line
    # FIXME anywhere where there is a free string we need to make sure it is in one line
    mutation = f"""
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
    return graphql_parse(mutation)


def duplicate_item_mutation(
    board_id: ID, item_id: ID, with_updates: bool | None = None, with_complexity: bool = False
) -> str:
    """
    This mutation creates a copy of an item on the same board, with the option to include updates.
    For more information, visit https://developer.monday.com/api-reference/reference/items#duplicate-an-item

    Args:
        board_id (ID): The ID of the board containing the item to duplicate.

        with_updates (bool): (Optional) Whether to include the item's updates in the duplication.

        item_id (ID): The ID of the item to duplicate.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def archive_item_mutation(item_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation archives an item, making it no longer visible in the active item list.
    For more information, visit https://developer.monday.com/api-reference/reference/items#archive-an-item
    Args:

        item_id (ID): The ID of the item to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_item_mutation(item_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation permanently removes an item from a board.
    For more information, visit https://developer.monday.com/api-reference/reference/items#delete-an-item

    Args:
        item_id (ID): The ID of the item to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(mutation)


def create_subitem_mutation(
    parent_item_id: ID,
    subitem_name: str,
    column_values: dict | None = None,
    create_labels_if_missing: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a new subitem under a specific parent item with a given name and optional column values.
    For more information, visit https://developer.monday.com/api-reference/reference/subitems#create-a-subitem

    Args:
        parent_item_id (ID): The ID of the parent item.

        subitem_name (str): The name of the new subitem.

        column_values (dict): (Optional) The column values for the new subitem in JSON format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def change_multiple_item_column_values_mutation(
    item_id: ID,
    board_id: ID,
    column_values: dict,
    create_labels_if_missing: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This mutation updates the values of multiple columns for a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-multiple-column-values

    Args:
        item_id (ID): The ID of the item to update.

        board_id (ID): The ID of the board containing the item.

        column_values (dict): The updated column values as a dictionary in a {column_id: column_value, ...} format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def change_item_column_json_value_mutation(
    item_id: ID,
    column_id: str,
    board_id: ID,
    value: dict,
    create_labels_if_missing: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This mutation updates the value of a specific column for an item using a JSON value. For more information, visit
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
    mutation = f"""
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
    return graphql_parse(mutation)


def change_item_column_simple_value_mutation(
    item_id: ID,
    column_id: str,
    board_id: ID,
    value: str,
    create_labels_if_missing: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This mutation updates the value of a specific column for an item using a simple string value.
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
    mutation = f"""
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
    return graphql_parse(mutation)


def upload_file_to_column_mutation(item_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This mutation uploads a file and adds it to a specific column of an item. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-file-to-the-file-column

    Args:
        item_id (ID): The ID of the item to add the file to.

        column_id (str): The unique identifier of the column to add the file to.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def clear_item_updates_mutation(item_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation removes all updates associated with a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/items#clear-an-items-updates

    Args:
        item_id (ID): The ID of the item to clear updates from.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        clear_item_updates (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(mutation)


def move_item_to_group_mutation(item_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This mutation moves an item to a different group within the same board. For more information, visit
    https://developer.monday.com/api-reference/reference/items#move-item-to-group

    Args:
        item_id (ID): The ID of the item to move.

        group_id (str): The ID of the target group within the board.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def move_item_to_board_mutation(
    board_id: ID,
    group_id: str,
    item_id: ID,
    columns_mapping: ColumnsMappingInput | list[dict[str, str]] = None,
    subitems_columns_mapping: ColumnsMappingInput | list[dict[str, str]] = None,
    with_complexity=False,
) -> str:
    """
    This mutation moves an item to a different board. For more information, visit
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
    mutation = f"""
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
    return graphql_parse(mutation)


__all__ = [
    "archive_item_mutation",
    "change_item_column_json_value_mutation",
    "change_item_column_simple_value_mutation",
    "change_multiple_item_column_values_mutation",
    "clear_item_updates_mutation",
    "create_item_mutation",
    "create_subitem_mutation",
    "delete_item_mutation",
    "duplicate_item_mutation",
    "move_item_to_board_mutation",
    "move_item_to_group_mutation",
    "upload_file_to_column_mutation",
]
