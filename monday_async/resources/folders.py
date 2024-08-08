from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (
    get_folders_query, create_folder_query, update_folder_query,
    delete_folder_query
)
from monday_async.types import FolderColor


ID = Union[int, str]


class FolderResource(AsyncBaseResource):
    async def get_folders(self, ids: Union[ID, List[ID]] = None,
                          workspace_ids: Union[ID, List[ID]] = None,
                          limit: int = 25, page: int = 1,
                          with_complexity: bool = False) -> dict:
        """
        Execute a query to retrieve folders, allowing you to specify specific folders,
            workspaces, limits, and pagination.

        For more information, visit https://developer.monday.com/api-reference/reference/folders#queries

        Parameters:
            ids (Union[ID, List[ID]]): (Optional) A single folder ID or a list of IDs to retrieve specific folders.
            workspace_ids (Union[ID, List[ID]]): (Optional) A single workspace ID or a list of IDs to filter folders
                by workspace. Use null to include the Main Workspace.
            limit (int): (Optional) The maximum number of folders to return. Default is 25, maximum is 100.
            page (int): (Optional) The page number to return. Starts at 1.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_folders_query(ids=ids, workspace_ids=workspace_ids, limit=limit, page=page,
                                  with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_folder(self, workspace_id: ID, name: str,
                            color: Optional[FolderColor] = FolderColor.NULL,
                            parent_folder_id: Optional[ID] = None,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to create a new folder within a specified workspace and parent folder (optional).

        For more information, visit https://developer.monday.com/api-reference/reference/folders#create-a-folder

        Parameters:
            workspace_id (ID): The unique identifier of the workspace where the folder will be created.
            name (str): The name of the new folder.
            color (FolderColor): (Optional) The color of the new folder, chosen from the FolderColor enum.
            parent_folder_id (ID): (Optional) The ID of the parent folder within the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_folder_query(workspace_id=workspace_id, name=name, color=color,
                                    parent_folder_id=parent_folder_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def update_folder(self, folder_id: ID, name: Optional[str] = None,
                            color: Optional[FolderColor] = None,
                            parent_folder_id: Optional[ID] = None,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to modify an existing folder's name, color, or parent folder.

        Parameters:
            folder_id (ID): The unique identifier of the folder to update.
            name (str): (Optional) The new name for the folder.
            color (FolderColor): (Optional) The new color for the folder, chosen from the FolderColor enum.
            parent_folder_id (ID): (Optional) The ID of the new parent folder for the folder.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = update_folder_query(folder_id=folder_id, name=name, color=color,
                                    parent_folder_id=parent_folder_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_folder(self, folder_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to permanently remove a folder from a workspace.

        Parameters:
            folder_id (ID): The unique identifier of the folder to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_folder_query(folder_id=folder_id, with_complexity=with_complexity)
        return await self.client.execute(query)
