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
from monday_async.types import ID, ColumnType


def create_column_mutation(
    board_id: ID,
    title: str,
    column_type: ColumnType,
    description: str | None = None,
    defaults: dict | None = None,
    column_id: str | None = None,
    after_column_id: ID | None = None,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a new column on a specific board with a specified title, type, and optional description,
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
    mutation = f"""
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
    return graphql_parse(mutation)


def change_column_title_mutation(board_id: ID, column_id: str, title: str, with_complexity: bool = False) -> str:
    """
    This mutation updates the title of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-column-title

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        title (str): The new title for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def change_column_description_mutation(
    board_id: ID, column_id: str, description: str, with_complexity: bool = False
) -> str:
    """
    This mutation updates the description of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-column-metadata

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        description (str): The new description for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def delete_column_mutation(board_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This mutation removes a column from a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#delete-a-column

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


__all__ = [
    "change_column_description_mutation",
    "change_column_title_mutation",
    "create_column_mutation",
    "delete_column_mutation",
]
