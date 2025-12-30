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

from typing import Union

from monday_async.graphql.mutations import (
    add_teams_to_workspace_mutation,
    add_users_to_workspace_mutation,
    create_workspace_mutation,
    delete_teams_from_workspace_mutation,
    delete_users_from_workspace_mutation,
    delete_workspace_mutation,
    update_workspace_mutation,
)
from monday_async.graphql.queries import get_workspaces_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import State, SubscriberKind, WorkspaceKind

ID = Union[int, str]


class WorkspaceResource(AsyncBaseResource):
    async def get_workspaces(
        self,
        workspace_ids: ID | list[ID] = None,
        limit: int = 25,
        page: int = 1,
        kind: WorkspaceKind | None = None,
        with_complexity: bool = False,
        state: State = State.ACTIVE,
    ) -> dict:
        """
        Execute a query to retrieve workspaces, offering filtering by IDs,
         kind, state, pagination, and optional complexity.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#queries

        Args:
            workspace_ids (Union[int, str, List[Union[int, str]]]): A single workspace ID, a list of workspace IDs, or
                None to get all workspaces.
            limit (int): The number of workspaces to return. The default is 25.
            page (int): The page number to get. Starts at 1.
            kind (WorkspaceKind): The kind of workspaces to return: open or closed.
            state (State): The state of workspaces you want to search by: all, active, archived, or deleted.
                The default is active.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = get_workspaces_query(
            workspace_ids=workspace_ids, limit=limit, page=page, kind=kind, with_complexity=with_complexity, state=state
        )
        return await self.client.execute(query)

    async def create_workspace(
        self,
        name: str,
        kind: WorkspaceKind,
        description: str | None = None,
        account_product_id: ID | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a workspace with a specified name, kind, and optional description.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#create-a-workspace

        Args:
            name (str): The new workspace name.
            kind (WorkspaceKind): The new workspace kind: open or closed.
            description (Optional[str]): The new workspace description.
            account_product_id (Optional[ID]): The unique identifier of the account's product
                in which to create the new workspace.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        mutation = create_workspace_mutation(
            name=name,
            kind=kind,
            description=description,
            account_product_id=account_product_id,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def update_workspace(
        self,
        workspace_id: ID,
        name: str | None = None,
        kind: WorkspaceKind | None = None,
        description: str | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to update a workspace's name, kind, or description.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#update-a-workspace

        Args:
            workspace_id (Union[int, str]): The unique identifier of the workspace to update.
            name (str): The updated workspace name.
            kind (WorkspaceKind): The kind of workspace to update: open or closed.
            description (Optional[str]): The updated workspace description.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        mutation = update_workspace_mutation(
            workspace_id=workspace_id, name=name, kind=kind, description=description, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def delete_workspace(self, workspace_id: int | str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to delete a workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#delete-a-workspace

        Args:
            workspace_id (Union[int, str]): The unique identifier of the workspace to delete.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        mutation = delete_workspace_mutation(workspace_id=workspace_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def add_users_to_workspace(
        self, workspace_id: ID, user_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to add users as subscribers or owners to a specific workspace.

        For more information, visit
        https://developer.monday.com/api-reference/reference/workspaces#add-users-to-a-workspace

        Args:
            workspace_id (ID): The unique identifier of the target workspace.
            user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to add to the workspace.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = add_users_to_workspace_mutation(workspace_id, user_ids, kind, with_complexity)
        return await self.client.execute(mutation)

    async def delete_users_from_workspace(
        self, workspace_id: ID, user_ids: ID | list[ID], with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to remove users from a specific workspace.

        For more information, visit
        https://developer.monday.com/api-reference/reference/workspaces#delete-users-from-a-workspace

        Args:
            workspace_id (ID): The unique identifier of the target workspace.
            user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to remove from the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_users_from_workspace_mutation(
            workspace_id=workspace_id, user_ids=user_ids, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def add_teams_to_workspace(
        self, workspace_id: ID, team_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to add teams as subscribers or owners to a specific workspace.

        For more information, visit
        https://developer.monday.com/api-reference/reference/workspaces#add-teams-to-a-workspace

        Args:
            workspace_id (ID): The unique identifier of the target workspace.
            team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to add to the workspace.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = add_teams_to_workspace_mutation(
            workspace_id=workspace_id, team_ids=team_ids, kind=kind, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def delete_teams_from_workspace(
        self, workspace_id: ID, team_ids: ID | list[ID], with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to remove teams from a specific workspace.

        For more information, visit
        https://developer.monday.com/api-reference/reference/workspaces#delete-teams-from-a-workspace

        Args:
            workspace_id (ID): The unique identifier of the target workspace.
            team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to remove from the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_teams_from_workspace_mutation(
            workspace_id=workspace_id, team_ids=team_ids, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)
