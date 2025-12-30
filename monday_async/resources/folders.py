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


from monday_async.graphql.mutations import create_folder_mutation, delete_folder_mutation, update_folder_mutation
from monday_async.graphql.queries import get_folders_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ID, FolderColor


class FolderResource(AsyncBaseResource):
    async def get_folders(
        self,
        ids: ID | list[ID] = None,
        workspace_ids: ID | list[ID] = None,
        limit: int = 25,
        page: int = 1,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve folders, allowing you to specify specific folders,
         workspaces, limits, and pagination.

        For more information, visit https://developer.monday.com/api-reference/reference/folders#queries

        Args:
            ids (Union[ID, List[ID]]): (Optional) A single folder ID or a list of IDs to retrieve specific folders.
            workspace_ids (Union[ID, List[ID]]): (Optional) A single workspace ID or a list of IDs to filter folders
                by workspace. Use null to include the Main Workspace.
            limit (int): (Optional) The maximum number of folders to return. Default is 25, maximum is 100.
            page (int): (Optional) The page number to return. Starts at 1.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_folders_query(
            ids=ids, workspace_ids=workspace_ids, limit=limit, page=page, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def create_folder(
        self,
        workspace_id: ID,
        name: str,
        color: FolderColor | None = FolderColor.NULL,
        parent_folder_id: ID | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a new folder within a specified workspace and parent folder (optional).

        For more information, visit https://developer.monday.com/api-reference/reference/folders#create-a-folder

        Args:
            workspace_id (ID): The unique identifier of the workspace where the folder will be created.
            name (str): The name of the new folder.
            color (FolderColor): (Optional) The color of the new folder, chosen from the FolderColor enum.
            parent_folder_id (ID): (Optional) The ID of the parent folder within the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = create_folder_mutation(
            workspace_id=workspace_id,
            name=name,
            color=color,
            parent_folder_id=parent_folder_id,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def update_folder(
        self,
        folder_id: ID,
        name: str | None = None,
        color: FolderColor | None = None,
        parent_folder_id: ID | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to modify an existing folder's name, color, or parent folder.

        Args:
            folder_id (ID): The unique identifier of the folder to update.
            name (str): (Optional) The new name for the folder.
            color (FolderColor): (Optional) The new color for the folder, chosen from the FolderColor enum.
            parent_folder_id (ID): (Optional) The ID of the new parent folder for the folder.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = update_folder_mutation(
            folder_id=folder_id,
            name=name,
            color=color,
            parent_folder_id=parent_folder_id,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def delete_folder(self, folder_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to permanently remove a folder from a workspace.

        Args:
            folder_id (ID): The unique identifier of the folder to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_folder_mutation(folder_id=folder_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)
