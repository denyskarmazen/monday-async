from typing import List, Union, Optional

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import UserKind
from monday_async.utils.queries import get_me_query, get_users_query, get_users_by_email_query


class UsersResource(AsyncBaseResource):
    async def get_me(self, with_complexity: bool = False) -> dict:
        """
        Get information about the user whose API key is being used. For more information, visit
        https://developer.monday.com/api-reference/reference/me#queries
        Args:
            with_complexity: Returns the complexity of the query with the query if set to True.
        """
        query = get_me_query(with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_users(self, user_ids: Union[int, str, List[Union[int, str]]] = None, limit: int = 50,
                        user_kind: UserKind = UserKind.ALL, newest_first: bool = False,
                        page: int = 1, with_complexity: bool = False) -> dict:
        """
        Get all users or get users by ids if provided. For more information, visit
        https://developer.monday.com/api-reference/reference/users#queries

        Args:
            user_ids (Union[int, str, List[Union[int, str]]]): A single user ID, a list of user IDs, or
                None to get all users.

            limit (int): The number of users to return, 50 by default.

            user_kind (UserKind): The kind of users you want to search by: all, non_guests, guests, or non_pending.

            newest_first (bool): Lists the most recently created users at the top.

            page (int): The page number to return. Starts at 1.

            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = get_users_query(user_ids=user_ids, limit=limit, user_kind=user_kind, newest_first=newest_first,
                                page=page, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_users_by_email(self, user_emails: Union[str, List[str]], user_kind: Optional[UserKind] = UserKind.ALL,
                                 newest_first: bool = False, with_complexity: bool = False) -> dict:
        """
        Get users by emails. For more information, visit
        https://developer.monday.com/api-reference/reference/users#queries

        Args:
            user_emails (Union[str, List[str]]): A single email of a user or a list of user emails.

            user_kind (UserKind): The kind of users you want to search by: all, non_guests, guests, or non_pending.

            newest_first (bool): Lists the most recently created users at the top.

            with_complexity (bool): Returns the complexity of the query with the query if set to True.
        """
        query = get_users_by_email_query(user_emails=user_emails, user_kind=user_kind, newest_first=newest_first,
                                         with_complexity=with_complexity)

        return await self.client.execute(query)
