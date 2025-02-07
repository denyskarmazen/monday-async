from enum import Enum
from typing import List, Union, Optional

from monday_async.types import FolderColor, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def get_folders_query(ids: Union[ID, List[ID]] = None, workspace_ids: Union[ID, List[ID]] = None,
                      limit: int = 25, page: int = 1, with_complexity: bool = False) -> str:
    """
    This query retrieves folders, allowing you to specify specific folders, workspaces, limits, and pagination.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#queries
    Args:
        ids (Union[ID, List[ID]]): (Optional) A single folder ID or a list of IDs to retrieve specific folders.

        workspace_ids (Union[ID, List[ID]]): (Optional) A single workspace ID or a list of IDs to filter folders
            by workspace. Use null to include the Main Workspace.

        limit (int): (Optional) The maximum number of folders to return. Default is 25, maximum is 100.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        folders (
            ids: {format_param_value(ids if ids else None)},
            workspace_ids: {format_param_value(workspace_ids if workspace_ids else None)},
            limit: {limit},
            page: {page}
        ) {{
            id
            name
            color
            parent {{
                id
                name
            }}
            sub_folders {{
                id
                name
            }}
            workspace {{
                id
                name
            }}

        }}
    }}
    """
    return graphql_parse(query)


def create_folder_query(workspace_id: ID, name: str, color: Optional[FolderColor] = FolderColor.NULL,
                        parent_folder_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new folder within a specified workspace and parent folder (optional).
    For more information, visit https://developer.monday.com/api-reference/reference/folders#create-a-folder

    Args:
        workspace_id (ID): The unique identifier of the workspace where the folder will be created.

        name (str): The name of the new folder.

        color (FolderColor): (Optional) The color of the new folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the parent folder within the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    color_value = color.value if isinstance(color, FolderColor) else color

    query = f"""
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
    return graphql_parse(query)


def update_folder_query(folder_id: ID, name: Optional[str] = None, color: Optional[FolderColor] = None,
                        parent_folder_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query modifies an existing folder's name, color, or parent folder.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#update-a-folder
    Args:
        folder_id (ID): The unique identifier of the folder to update.

        name (str): (Optional) The new name for the folder.

        color (FolderColor): (Optional) The new color for the folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the new parent folder for the folder.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    update_params = [
        value for value in [
            f"name: {format_param_value(name)}" if name else None,
            f"color: {color.value if isinstance(color, Enum) else color}" if color else None,
            f"parent_folder_id: {format_param_value(parent_folder_id)}" if parent_folder_id else None
        ] if value is not None
    ]

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_folder (
            folder_id: {format_param_value(folder_id)},
            {', '.join(update_params)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


def delete_folder_query(folder_id: ID, with_complexity: bool = False) -> str:
    """
    This query permanently removes a folder from a workspace.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#delete-a-folder

    Args:
        folder_id (ID): The unique identifier of the folder to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_folder (folder_id: {format_param_value(folder_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_folders_query',
    'create_folder_query',
    'update_folder_query',
    'delete_folder_query'
]
