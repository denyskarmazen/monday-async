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


from typing import Optional

from monday_async.graphql.mutations import (
    activate_users_mutation,
    deactivate_users_mutation,
    invite_users_mutation,
    update_multiple_users_mutation,
    update_users_email_domain_mutation,
    update_users_role_mutation,
)
from monday_async.graphql.queries import get_me_query, get_users_by_email_query, get_users_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ID, BaseRoleName, Product, UserKind
from monday_async.types.args import UserAttributesInput


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

    async def get_users(
        self,
        user_ids: Optional[int | str | list[int | str]] = None,
        limit: int = 50,
        user_kind: UserKind = UserKind.ALL,
        newest_first: bool = False,
        page: int = 1,
        with_complexity: bool = False,
    ) -> dict:
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
        query = get_users_query(
            user_ids=user_ids,
            limit=limit,
            user_kind=user_kind,
            newest_first=newest_first,
            page=page,
            with_complexity=with_complexity,
        )
        return await self.client.execute(query)

    async def get_users_by_email(
        self,
        user_emails: str | list[str],
        user_kind: UserKind | None = UserKind.ALL,
        newest_first: bool = False,
        with_complexity: bool = False,
    ) -> dict:
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
        query = get_users_by_email_query(
            user_emails=user_emails, user_kind=user_kind, newest_first=newest_first, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def update_users_role(
        self, user_ids: ID | list[ID], new_role: BaseRoleName | str, with_complexity: bool = False
    ) -> dict:
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

    async def deactivate_users(self, user_ids: ID | list[ID], with_complexity: bool = False) -> dict:
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

    async def activate_users(self, user_ids: ID | list[ID], with_complexity: bool = False) -> dict:
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

    async def update_users_email_domain(
        self, new_domain: str, user_ids: ID | list[ID], with_complexity: bool = False
    ) -> dict:
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
        mutation = update_users_email_domain_mutation(
            new_domain=new_domain, user_ids=user_ids, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def invite_users(
        self,
        emails: str | list[str],
        product: Product | str,
        user_role: BaseRoleName | str,
        with_complexity: bool = False,
    ) -> dict:
        """
        Invite users to join a monday.com account. Invited users will be in a pending status until they accept.

        For more information, visit
        https://developer.monday.com/api-reference/reference/users#invite-users

        Args:
            emails (Union[str, List[str]]): The email addresses of users to invite.
            product (Union[Product, str]): The product to invite users to.
                Valid values: Product.CRM, Product.DEV, Product.FORMS, Product.KNOWLEDGE,
                Product.SERVICE, Product.WHITEBOARD, Product.WORKFLOWS, Product.WORK_MANAGEMENT
            user_role (Union[BaseRoleName, str]): The role to assign to invited users.
                Valid values: BaseRoleName.ADMIN, BaseRoleName.MEMBER, BaseRoleName.VIEWER, BaseRoleName.GUEST
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API containing invited_users and any errors.
        """
        mutation = invite_users_mutation(
            emails=emails, product=product, user_role=user_role, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def update_multiple_users(
        self,
        user_updates: list[tuple[ID, UserAttributesInput]],
        with_complexity: bool = False,
    ) -> dict:
        """
        Update multiple users' attributes. For more information, visit
        https://developer.monday.com/api-reference/reference/users#update-multiple-users

        Args:
            user_updates (List[Tuple[ID, UserAttributesInput]]): A list of tuples, each containing a user ID
                and a UserAttributesInput object specifying the attributes to update.
                Example: [(123, UserAttributesInput(name="New Name")), (456, UserAttributesInput(title="Manager"))]
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The response from the API containing updated_users and any errors.
        """
        mutation = update_multiple_users_mutation(user_updates=user_updates, with_complexity=with_complexity)
        return await self.client.execute(mutation)
