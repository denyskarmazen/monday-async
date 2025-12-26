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

from enum import Enum
from typing import Any

from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, GroupAttributes, GroupColors, GroupUpdateColors, PositionRelative


def create_group_mutation(
    board_id: ID,
    group_name: str,
    group_color: GroupColors | str | None = None,
    relative_to: str | None = None,
    position_relative_method: PositionRelative | None = None,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a new group on a specific board with a specified name and positioning
    relative to other groups.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#create-a-group

    Args:
        board_id (ID): The ID of the board to create the group on.

        group_name (str): The name of the new group.

        group_color (Optional[Union[GroupColors, str]]): The group's color. Pass as a HEX value when passing as a string
            For some reason currently not all colors work.

        relative_to (str): (Optional) The ID of the group to position the new group relative to.

        position_relative_method (PositionRelative): (Optional) The method for positioning the new group:
            before_at or after_at.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if position_relative_method:
        position_relative_method_value = (
            position_relative_method.value
            if isinstance(position_relative_method, PositionRelative)
            else position_relative_method
        )
    else:
        position_relative_method_value = "null"

    group_color_value = group_color.value if isinstance(group_color, GroupColors) else group_color
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_group (
            board_id: {format_param_value(board_id)},
            group_name: {format_param_value(group_name)},
            group_color: {format_param_value(group_color_value)},
            relative_to: {format_param_value(relative_to)},
            position_relative_method: {position_relative_method_value}
        ) {{
            id
            title
            color
        }}
    }}
    """
    return graphql_parse(mutation)


def update_group_mutation(
    board_id: ID,
    group_id: str,
    group_attribute: GroupAttributes,
    new_value: Any | GroupUpdateColors,
    with_complexity: bool = False,
) -> str:
    """
    This mutation modifies an existing group's title, color, or position on the board.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#update-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to update.

        group_attribute (GroupAttributes): The attribute of the group to update: title, color,
            relative_position_after, or relative_position_before.

        new_value (str): The new value for the specified group attribute.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    group_attribute_value = group_attribute.value if isinstance(group_attribute, GroupAttributes) else group_attribute
    group_new_value = new_value.value if isinstance(new_value, Enum) else new_value
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            group_attribute: {group_attribute_value},
            new_value: {format_param_value(group_new_value)}
        ) {{
            id
            title
            color
            position
        }}
    }}
    """
    return graphql_parse(mutation)


def duplicate_group_mutation(
    board_id: ID,
    group_id: str,
    add_to_top: bool | None = None,
    group_title: str | None = None,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a copy of a group within the same board,
        with options to position the new group and set its title.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#duplicate-group

    Args:
        board_id (ID): The ID of the board containing the group to duplicate.

        group_id (str): The unique identifier of the group to duplicate.

        add_to_top (bool): (Optional) Whether to add the new group to the top of the board.

        group_title (str): (Optional) The title for the new duplicated group.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        duplicate_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            add_to_top: {format_param_value(add_to_top)},
            group_title: {format_param_value(group_title)}
        ) {{
            id
            title
            color
            position
        }}
    }}
    """
    return graphql_parse(mutation)


def archive_group_mutation(board_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This mutation archives a group on a specific board, removing it from the active view. For more information, visit
    https://developer.monday.com/api-reference/reference/groups#archive-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_group_mutation(board_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This mutation permanently removes a group from a board. For more information, visit
    https://developer.monday.com/api-reference/reference/groups#delete-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = [
    "archive_group_mutation",
    "create_group_mutation",
    "delete_group_mutation",
    "duplicate_group_mutation",
    "update_group_mutation",
]
