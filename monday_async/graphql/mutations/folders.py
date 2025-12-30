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

from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, FolderColor


def create_folder_mutation(
    workspace_id: ID,
    name: str,
    color: FolderColor | None = FolderColor.NULL,
    parent_folder_id: ID | None = None,
    with_complexity: bool = False,
) -> str:
    """
    This mutation creates a new folder within a specified workspace and parent folder (optional).
    For more information, visit https://developer.monday.com/api-reference/reference/folders#create-a-folder

    Args:
        workspace_id (ID): The unique identifier of the workspace where the folder will be created.

        name (str): The name of the new folder.

        color (FolderColor): (Optional) The color of the new folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the parent folder within the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    color_value = color.value if isinstance(color, FolderColor) else color

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_folder (
            workspace_id: {format_param_value(workspace_id)},
            name: {format_param_value(name)},
            color: {color_value},
            parent_folder_id: {format_param_value(parent_folder_id)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(mutation)


def update_folder_mutation(
    folder_id: ID,
    name: str | None = None,
    color: FolderColor | None = None,
    parent_folder_id: ID | None = None,
    with_complexity: bool = False,
) -> str:
    """
    This mutation modifies an existing folder's name, color, or parent folder.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#update-a-folder
    Args:
        folder_id (ID): The unique identifier of the folder to update.

        name (str): (Optional) The new name for the folder.

        color (FolderColor): (Optional) The new color for the folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the new parent folder for the folder.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    update_params = [
        value
        for value in [
            f"name: {format_param_value(name)}" if name else None,
            f"color: {color.value if isinstance(color, Enum) else color}" if color else None,
            f"parent_folder_id: {format_param_value(parent_folder_id)}" if parent_folder_id else None,
        ]
        if value is not None
    ]

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_folder (
            folder_id: {format_param_value(folder_id)},
            {", ".join(update_params)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_folder_mutation(folder_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation permanently removes a folder from a workspace.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#delete-a-folder

    Args:
        folder_id (ID): The unique identifier of the folder to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_folder (folder_id: {format_param_value(folder_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = ["create_folder_mutation", "delete_folder_mutation", "update_folder_mutation"]
