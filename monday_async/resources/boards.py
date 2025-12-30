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


from monday_async.graphql.mutations import (
    add_teams_to_board_mutation,
    add_users_to_board_mutation,
    archive_board_mutation,
    create_board_mutation,
    delete_board_mutation,
    delete_teams_from_board_mutation,
    duplicate_board_mutation,
    remove_users_from_board_mutation,
    update_board_mutation,
)
from monday_async.graphql.queries import get_board_views_query, get_boards_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ID, BoardAttributes, BoardKind, BoardsOrderBy, DuplicateBoardType, State, SubscriberKind


class BoardResource(AsyncBaseResource):
    async def get_boards(
        self,
        ids: ID | list[ID] = None,
        board_kind: BoardKind | None = None,
        state: State = State.ACTIVE,
        workspace_ids: ID | list[ID] = None,
        order_by: BoardsOrderBy | None = None,
        limit: int = 25,
        page: int = 1,
        with_columns: bool = True,
        with_groups: bool = True,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve boards, offering filtering by IDs, board kind, state, workspace,
         and ordering options.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#queries

        Args:
            ids (List[ID]): (Optional) A list of board IDs to retrieve specific boards.
            board_kind (BoardKind): (Optional) The kind of boards to retrieve: public, private, or share.
            state (State): (Optional) The state of the boards: all, active, archived, or deleted. Defaults to active.
            workspace_ids (List[ID]): (Optional) A list of workspace IDs to filter boards by specific workspaces.
            order_by (BoardsOrderBy): (Optional) The property to order the results by: created_at or used_at.
            limit (int): (Optional) The maximum number of boards to return. Defaults to 25.
            page (int): (Optional) The page number to return. Starts at 1.
            with_columns (bool): (Optional) Set to True to include columns in the query results.
            with_groups (bool): (Optional) Set to True to include groups in the query results.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_boards_query(
            ids=ids,
            board_kind=board_kind,
            state=state,
            workspace_ids=workspace_ids,
            order_by=order_by,
            limit=limit,
            page=page,
            with_columns=with_columns,
            with_groups=with_groups,
            with_complexity=with_complexity,
        )
        return await self.client.execute(query)

    async def create_board(
        self,
        board_name: str,
        board_kind: BoardKind,
        description: str | None = None,
        folder_id: ID | None = None,
        workspace_id: ID | None = None,
        template_id: ID | None = None,
        board_owner_ids: list[ID] | None = None,
        board_owner_team_ids: list[ID] | None = None,
        board_subscriber_ids: list[ID] | None = None,
        board_subscriber_teams_ids: list[ID] | None = None,
        empty: bool = False,
        with_columns: bool = False,
        with_groups: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a new board with specified name, kind, and optional description, folder, workspace,
         template, and subscribers/owners.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#create-a-board

        Args:
            board_name (str): The name of the new board.
            board_kind (BoardKind): The kind of board to create: public, private, or share.
            description (str): (Optional) A description for the new board.
            folder_id (ID): (Optional) The ID of the folder to create the board in.
            workspace_id (ID): (Optional) The ID of the workspace to create the board in.
            template_id (ID): (Optional) The ID of a board template to use for the new board's structure.
            board_owner_ids (List[ID]): (Optional) A list of user IDs to assign as board owners.
            board_owner_team_ids (List[ID]): (Optional) A list of team IDs to assign as board owners.
            board_subscriber_ids (List[ID]): (Optional) A list of user IDs to subscribe to the board.
            board_subscriber_teams_ids (List[ID]): (Optional) A list of team IDs to subscribe to the board.
            empty (bool): (Optional) Set to True to create an empty board without default items. Defaults to False.
            with_columns (bool): (Optional) Set to True to include columns in the query results. Defaults to False.
            with_groups (bool): (Optional) Set to True to include groups in the query results. Defaults to False.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = create_board_mutation(
            board_name=board_name,
            board_kind=board_kind,
            description=description,
            folder_id=folder_id,
            workspace_id=workspace_id,
            template_id=template_id,
            board_owner_ids=board_owner_ids,
            board_owner_team_ids=board_owner_team_ids,
            board_subscriber_ids=board_subscriber_ids,
            board_subscriber_teams_ids=board_subscriber_teams_ids,
            empty=empty,
            with_columns=with_columns,
            with_groups=with_groups,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def duplicate_board(
        self,
        board_id: ID,
        duplicate_type: DuplicateBoardType,
        board_name: str | None = None,
        workspace_id: ID | None = None,
        folder_id: ID | None = None,
        keep_subscribers: bool = False,
        with_columns: bool = False,
        with_groups: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to duplicate a board with options to include structure, items, updates, and subscribers.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#duplicate-a-board

        Args:
            board_id (ID): The ID of the board to duplicate.
            duplicate_type (DuplicateBoardType): The type of duplication: duplicate_board_with_structure,
            duplicate_board_with_pulses, or duplicate_board_with_pulses_and_updates.
            board_name (str): (Optional) The name for the new duplicated board.
                If omitted, a name is automatically generated.
            workspace_id (ID): (Optional) The ID of the workspace to place the duplicated board in.
                Defaults to the original board's workspace.
            folder_id (ID): (Optional) The ID of the folder to place the duplicated board in.
                Defaults to the original board's folder.
            keep_subscribers (bool): (Optional) Whether to copy subscribers to the new board. Defaults to False.
            with_columns (bool): (Optional) Set to True to include columns in the query results. Defaults to False.
            with_groups (bool): (Optional) Set to True to include groups in the query results. Defaults to False.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = duplicate_board_mutation(
            board_id=board_id,
            duplicate_type=duplicate_type,
            board_name=board_name,
            workspace_id=workspace_id,
            folder_id=folder_id,
            keep_subscribers=keep_subscribers,
            with_columns=with_columns,
            with_groups=with_groups,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def update_board(
        self, board_id: ID, board_attribute: BoardAttributes, new_value: str, with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to update a board attribute.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#update-a-board

        Args:
            board_id (ID): The ID of a board to update
            board_attribute (BoardAttributes): The board's attribute to update: name, description, or communication.
            new_value (str): The new attribute value
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = update_board_mutation(
            board_id=board_id, board_attribute=board_attribute, new_value=new_value, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def archive_board(self, board_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to archive a board, making it no longer visible in the active board list.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#archive-a-board

        Args:
            board_id (ID): The ID of the board to archive.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = archive_board_mutation(board_id=board_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def delete_board(self, board_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to permanently delete a board.

        For more information, visit https://developer.monday.com/api-reference/reference/boards#delete-a-board

        Args:
            board_id (ID): The ID of the board to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_board_mutation(board_id=board_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def add_users_to_board(
        self, board_id: ID, user_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
    ) -> str:
        """
        Execute a mutation to add users as subscribers or owners to a board.

        For more information, visit https://developer.monday.com/api-reference/reference/users#add-users-to-a-board

        Args:
            board_id (ID): The ID of the board to add users to.
            user_ids (Union[ID, List[ID]]): A list of user IDs to add as subscribers or owners.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = add_users_to_board_mutation(
            board_id=board_id, user_ids=user_ids, kind=kind, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def remove_users_from_board(
        self, board_id: ID, user_ids: ID | list[ID], with_complexity: bool = False
    ) -> dict:
        """
        Execute a query to remove users from a board's subscribers or owners.

        For more information, visit
         https://developer.monday.com/api-reference/reference/users#delete-subscribers-from-a-board

        Args:
            board_id (ID): The ID of the board to remove users from.
            user_ids (Union[ID, List[ID]]): A list of user IDs to remove from the board.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = remove_users_from_board_mutation(
            board_id=board_id, user_ids=user_ids, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def add_teams_to_board(
        self, board_id: ID, team_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
    ) -> dict:
        """
        Execute a query to add teams as subscribers or owners to a board.

        For more information, visit https://developer.monday.com/api-reference/reference/teams#add-teams-to-a-board

        Args:
            board_id (ID): The ID of the board to add teams to.
            team_ids (Union[ID, List[ID]]): A list of team IDs to add as subscribers or owners.
            kind (SubscriberKind): The type of subscription to grant: subscriber or owner.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = add_teams_to_board_mutation(
            board_id=board_id, team_ids=team_ids, kind=kind, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def delete_teams_from_board(
        self, board_id: ID, team_ids: ID | list[ID], with_complexity: bool = False
    ) -> dict:
        """
        Execute a query to remove teams from a board's subscribers or owners.

        For more information, visit https://developer.monday.com/api-reference/reference/teams#delete-teams-from-a-board

        Args:
            board_id (ID): The ID of the board to remove teams from.
            team_ids (Union[ID, List[ID]]): A list of team IDs to remove from the board.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_teams_from_board_mutation(
            board_id=board_id, team_ids=team_ids, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def get_board_views(
        self,
        board_id: ID,
        ids: ID | list[ID] = None,
        view_type: str | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve the views associated with a specific board.

        For more information, visit https://developer.monday.com/api-reference/reference/board-views#queries

        Args:
            board_id (ID): The ID of the board to retrieve views from.
            ids (Union[ID, List[ID]]): (Optional) A list of view IDs to retrieve specific views.
            view_type (str): (Optional) The type of views to retrieve.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_board_views_query(board_id=board_id, ids=ids, view_type=view_type, with_complexity=with_complexity)
        return await self.client.execute(query)
