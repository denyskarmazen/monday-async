from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (get_me_query, get_users_query, get_users_by_email_query, get_teams_query,
                                        add_users_to_team_query, remove_users_from_team_query)
from monday_async.utils.types import UserKind


class UsersResource(AsyncBaseResource):
    async def get_me(self, with_complexity: bool = False):
        query = get_me_query(with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_users(self, user_ids: Union[int, str, List[Union[int, str]]] = None, limit: int = 50,
                        user_kind: UserKind = UserKind.ALL, newest_first: bool = False,
                        page: int = 1, with_complexity: bool = False):
        query = get_users_query(user_ids=user_ids, limit=limit, user_kind=user_kind, newest_first=newest_first,
                                page=page, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_users_by_email(self, user_emails: Union[str, List[str]], user_kind: Optional[UserKind] = UserKind.ALL,
                                 newest_first: bool = False, with_complexity: bool = False):
        query = get_users_by_email_query(user_emails=user_emails, user_kind=user_kind, newest_first=newest_first,
                                         with_complexity=with_complexity)

        return await self.client.execute(query)

    async def get_teams(self, team_ids: Union[int, str, List[Union[int, str]]] = None, with_complexity: bool = False):
        query = get_teams_query(team_ids=team_ids, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def add_users_to_team(self, team_id: Union[int, str], user_ids: Union[int, str, List[Union[int, str]]],
                                with_complexity: bool = False):
        query = add_users_to_team_query(team_id=team_id, user_ids=user_ids, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def remove_users_from_team(self, team_id: Union[int, str], user_ids: Union[int, str, List[Union[int, str]]],
                                     with_complexity: bool = False):
        query = remove_users_from_team_query(team_id=team_id, user_ids=user_ids, with_complexity=with_complexity)
        return await self.client.execute(query)