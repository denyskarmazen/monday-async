from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (
    get_workspaces_query, create_workspace_query, update_workspace_query,
    delete_workspace_query, add_users_to_workspace_query, delete_users_from_workspace_query,
    add_teams_to_workspace_query, delete_teams_from_workspace_query,
)
from monday_async.utils.types import WorkspaceKind, State, SubscriberKind


ID = Union[int, str]


class WorkspaceResource(AsyncBaseResource):
    async def get_workspaces(self, workspace_ids: Union[ID, List[ID]] = None,
                             limit: int = 25, page: int = 1,
                             kind: Optional[WorkspaceKind] = None,
                             with_complexity: bool = False,
                             state: State = State.ACTIVE):
        """
        Execute a query to retrieve workspaces, offering filtering by IDs,
        kind, state, pagination, and optional complexity.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#queries

        Parameters:
            workspace_ids (Union[int, str, List[Union[int, str]]]): A single workspace ID, a list of workspace IDs, or
                None to get all workspaces.
            limit (int): The number of workspaces to return. The default is 25.
            page (int): The page number to get. Starts at 1.
            kind (WorkspaceKind): The kind of workspaces to return: open or closed.
            state (State): The state of workspaces you want to search by: all, active, archived, or deleted.
                The default is active.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = get_workspaces_query(workspace_ids=workspace_ids, limit=limit, page=page, kind=kind,
                                     with_complexity=with_complexity, state=state)
        return await self.client.execute(query)

    async def create_workspace(self, name: str, kind: WorkspaceKind,
                               description: Optional[str] = None,
                               with_complexity: bool = False):
        """
        Execute a query to create a workspace with a specified name, kind, and optional description.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#create-a-workspace

        Parameters:
            name (str): The new workspace name.
            kind (WorkspaceKind): The new workspace kind: open or closed.
            description (Optional[str]): The new workspace description.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = create_workspace_query(name=name, kind=kind, description=description, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def update_workspace(self, workspace_id: ID,
                               name: Optional[str] = None,
                               kind: Optional[WorkspaceKind] = None,
                               description: Optional[str] = None,
                               with_complexity: bool = False):
        """
        Execute a query to update a workspace's name, kind, or description.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#update-a-workspace

        Parameters:
            workspace_id (Union[int, str]): The unique identifier of the workspace to update.
            name (str): The updated workspace name.
            kind (WorkspaceKind): The kind of workspace to update: open or closed.
            description (Optional[str]): The updated workspace description.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = update_workspace_query(workspace_id=workspace_id, name=name, kind=kind, description=description,
                                       with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_workspace(self, workspace_id: Union[int, str],
                               with_complexity: bool = False):
        """
        Executes a query to delete a workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#delete-a-workspace

        Parameters:
            workspace_id (Union[int, str]): The unique identifier of the workspace to delete.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = delete_workspace_query(workspace_id=workspace_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def add_users_to_workspace(self, workspace_id: ID, user_ids: Union[ID, List[ID]],
                                     kind: SubscriberKind, with_complexity: bool = False) -> str:
        """
        Execute a query to add users as subscribers or owners to a specific workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#add-users-to-a-workspace

        Parameters:
            workspace_id (ID): The unique identifier of the target workspace.
            user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to add to the workspace.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = add_users_to_workspace_query(workspace_id, user_ids, kind, with_complexity)
        return await self.client.execute(query)

    async def delete_users_from_workspace(self, workspace_id: ID, user_ids: Union[ID, List[ID]],
                                          with_complexity: bool = False) -> str:
        """
        Execute a query to remove users from a specific workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#delete-users-from-a-workspace

        Parameters:
            workspace_id (ID): The unique identifier of the target workspace.
            user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to remove from the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_users_from_workspace_query(workspace_id=workspace_id, user_ids=user_ids,
                                                  with_complexity=with_complexity)
        return await self.client.execute(query)

    async def add_teams_to_workspace(self, workspace_id: ID, team_ids: Union[ID, List[ID]],
                                     kind: SubscriberKind, with_complexity: bool = False) -> str:
        """
        Execute a query to add teams as subscribers or owners to a specific workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#add-teams-to-a-workspace

        Parameters:
            workspace_id (ID): The unique identifier of the target workspace.
            team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to add to the workspace.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = add_teams_to_workspace_query(workspace_id=workspace_id, team_ids=team_ids, kind=kind,
                                             with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_teams_from_workspace(self, workspace_id: ID, team_ids: Union[ID, List[ID]],
                                          with_complexity: bool = False) -> str:
        """
        Executes a query to remove teams from a specific workspace.

        For more information, visit https://developer.monday.com/api-reference/reference/workspaces#delete-teams-from-a-workspace

        Parameters:
            workspace_id (ID): The unique identifier of the target workspace.
            team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to remove from the workspace.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_teams_from_workspace_query(workspace_id=workspace_id, team_ids=team_ids,
                                                  with_complexity=with_complexity)
        return await self.client.execute(query)
