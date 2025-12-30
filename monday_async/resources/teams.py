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
    add_users_to_team_mutation,
    assign_team_owners_mutation,
    create_team_mutation,
    delete_team_mutation,
    remove_team_owners_mutation,
    remove_users_from_team_mutation,
)
from monday_async.graphql.queries import get_teams_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ID


class TeamsResource(AsyncBaseResource):
    async def get_teams(
        self, team_ids: int | str | list[int | str] | None = None, with_complexity: bool = False
    ) -> dict:
        """
        Get all teams or get teams by ids if provided. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#queries

        Args:
            team_ids (Union[int, str, List[Union[int, str]]]): A single team ID, a list of team IDs, or
                None to get all teams.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = get_teams_query(team_ids=team_ids, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_team(
        self,
        name: str,
        subscriber_ids: list[ID] | None = None,
        parent_team_id: ID | None = None,
        is_quest_team: bool = False,
        allow_empty_teams: bool = True,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a team. For more information,
        visit https://developer.monday.com/api-reference/reference/teams#create-team

        Args:
            name (str): The new team's name.
            subscriber_ids (Optional[List[ID]]): The team member's unique identifiers.
                Cannot be empty unless allow_empty_team is set to True.
            parent_team_id (Optional[ID]): The parent team's unique identifier.
            is_quest_team (bool): Whether or not the new team contains guest users. False by default.
            allow_empty_teams (bool): Whether or not the team can have no subscribers. True by default.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = create_team_mutation(
            name=name,
            subscriber_ids=subscriber_ids,
            parent_team_id=parent_team_id,
            is_quest_team=is_quest_team,
            allow_empty_teams=allow_empty_teams,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def delete_team(self, team_id: int | str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to delete a team. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#delete-team

        Args:
            team_id (Union[int, str]): The unique identifier of the team to delete.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = delete_team_mutation(team_id=team_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def add_users_to_team(
        self, team_id: int | str, user_ids: int | str | list[int | str], with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to add users to a team. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#add-users-to-a-team

        Args:
            team_id (Union[int, str]): The unique identifier of the team to add users to.
            user_ids (Union[int, str, List[Union[int, str]]]): A single user ID of a user or a list of user IDs.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = add_users_to_team_mutation(team_id=team_id, user_ids=user_ids, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def remove_users_from_team(
        self, team_id: int | str, user_ids: int | str | list[int | str], with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to remove users from a team. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#remove-users-from-a-team

        Args:
            team_id (Union[int, str]): The unique identifier of the team to remove users from.
            user_ids (Union[int, str, List[Union[int, str]]]): A single user ID of a user or a list of user IDs.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = remove_users_from_team_mutation(user_ids=user_ids, team_id=team_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def assign_team_owners(self, user_ids: ID | list[ID], team_id: ID, with_complexity: bool = False):
        """
        Execute a mutation to assign team owners to a team. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#assign-team-owners

        Args:
            user_ids (Union[ID, List[ID]]): A single user ID of a user or a list of user IDs.
            team_id (ID): The unique identifier of the team to assign owners to.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        Returns:
            dict: The response from the API.
        """
        mutation = assign_team_owners_mutation(user_ids=user_ids, team_id=team_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def remove_team_owners(self, user_ids: ID | list[ID], team_id: ID, with_complexity: bool = False):
        """
        Execute a mutation to remove owners from a team. For more information, visit
        https://developer.monday.com/api-reference/reference/teams#remove-team-owners

        Args:
            user_ids (Union[ID, List[ID]]): A single user ID of a user or a list of user IDs.
            team_id (ID): The unique identifier of the team to assign owners to.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        Returns:
            dict: The response from the API.
        """
        mutation = remove_team_owners_mutation(user_ids=user_ids, team_id=team_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)
