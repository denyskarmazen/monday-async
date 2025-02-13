from typing import List, Union, Optional

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import UserKind, ID, BaseRoleName
from monday_async.utils.queries import (get_me_query, get_users_query, get_users_by_email_query,
                                        deactivate_users_mutation, activate_users_mutation,
                                        update_users_email_domain_mutation)
from monday_async.utils.queries.user_queries import update_users_role_mutation


class UsersResource(AsyncBaseResource):
    async def get_me(self, with_complexity: bool = False) -> dict:
        """
        Get information about the user whose API key is being used. For more information, visit
        https://developer.monday.com/api-reference/reference/me#queries

        Args:
            with_complexity: Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
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

        Returns:
            dict: The response from the API.
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

        Returns:
            dict: The response from the API.
        """
        query = get_users_by_email_query(user_emails=user_emails, user_kind=user_kind, newest_first=newest_first,
                                         with_complexity=with_complexity)
        return await self.client.execute(query)

    async def update_users_role(self, user_ids: Union[ID, List[ID]], new_role: Union[BaseRoleName, str],
                                with_complexity: bool = False) -> dict:
        """
        Update a user's role. For more information, visit
        https://developer.monday.com/api-reference/reference/users#update-a-users-role

        Args:
            user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
            new_role (Union[BaseRoleName, str]): The user's updated role.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = update_users_role_mutation(user_ids=user_ids, new_role=new_role, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def deactivate_users(self, user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> dict:
        """
        Deactivates users from a monday.com account. For more information, visit
        https://developer.monday.com/api-reference/reference/users#deactivate-users

        Args:
            user_ids (Union[ID, List[ID]]): The unique identifiers of the users to deactivate. The maximum is 200.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = deactivate_users_mutation(user_ids=user_ids, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def activate_users(self, user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> dict:
        """
        Re-activate users in a monday.com account. For more information, visit
        https://developer.monday.com/api-reference/reference/users#activate-users

        Args:
            user_ids (Union[ID, List[ID]]): The unique identifiers of the users to activate. The maximum is 200.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = activate_users_mutation(user_ids=user_ids, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def update_users_email_domain(self, new_domain: str, user_ids: Union[ID, List[ID]],
                                        with_complexity: bool = False) -> dict:
        """
        Update a user's email domain. For more information, visit
        https://developer.monday.com/api-reference/reference/users#update-a-users-email-domain

        Args:
            new_domain (str): The updated email domain.
            user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API.
        """
        mutation = update_users_email_domain_mutation(new_domain=new_domain, user_ids=user_ids,
                                                      with_complexity=with_complexity)
        return await self.client.execute(mutation)
