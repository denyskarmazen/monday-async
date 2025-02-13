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

from typing import List, Union

from monday_async.types import UserKind, ID, BaseRoleName
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def get_me_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get data about the user connected to the API key that is used. For more information, visit
    https://developer.monday.com/api-reference/reference/me#queries

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL query.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        me {{
            id
            name
            title
            location
            phone
            teams {{
                id
                 name
            }}
            url
            is_admin
            is_guest
            is_view_only
            is_pending
        }}
    }}
    """
    return graphql_parse(query)


def get_users_query(user_ids: Union[ID, List[ID]] = None, limit: int = 50, user_kind: UserKind = UserKind.ALL,
                    newest_first: bool = False, page: int = 1, with_complexity: bool = False) -> str:
    """
    Construct a query to get all users or get users by ids if provided. For more information, visit
    https://developer.monday.com/api-reference/reference/users#queries

    Args:
        user_ids (Union[ID, List[ID]): A single user ID, a list of user IDs, or None to get all users.
        limit (int): The number of users to return, 50 by default.
        user_kind (UserKind): The kind of users you want to search by: all, non_guests, guests, or non_pending.
        newest_first (bool): Lists the most recently created users at the top.
        page (int): The page number to return. Starts at 1.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL query.
    """
    # Setting the limit based on the amount of user ids passed
    if user_ids and isinstance(user_ids, list):
        limit = len(user_ids)
    user_type_value = user_kind.value if isinstance(user_kind, UserKind) else user_kind
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        users (
            ids: {format_param_value(user_ids if user_ids else None)},
             limit: {limit},
             kind: {user_type_value},
             newest_first: {format_param_value(newest_first)},
            page: {page}
        ) {{
            id
            email
            name
            title
            location
            phone
            teams {{
                id
                 name
            }}
            url
            is_admin
            is_guest
            is_view_only
            is_pending
        }}
    }}
    """
    return graphql_parse(query)


def get_users_by_email_query(user_emails: Union[str, List[str]], user_kind: UserKind = UserKind.ALL,
                             newest_first: bool = False, with_complexity: bool = False) -> str:
    """
    Construct a query to get users by emails. For more information, visit
    https://developer.monday.com/api-reference/reference/users#queries

    Args:
        user_emails (Union[str, List[str]]): A single email of a user or a list of user emails.
        user_kind (UserKind): The kind of users you want to search by: all, non_guests, guests, or non_pending.
        newest_first (bool): Lists the most recently created users at the top.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL query.
    """
    # Setting the limit based on the amount of user ids passed
    if user_emails and isinstance(user_emails, list):
        limit = len(user_emails)
    else:
        limit = 1
    user_type_value = user_kind.value if isinstance(user_kind, UserKind) else user_kind
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        users (
            emails: {format_param_value(user_emails)},
             limit: {limit},
             kind: {user_type_value},
             newest_first: {str(newest_first).lower()},
        ) {{
            id
            email
            name
            title
            location
            phone
            teams {{
                id
                 name
            }}
            url
            is_admin
            is_guest
            is_view_only
            is_pending
        }}
    }}
    """
    return graphql_parse(query)


def update_users_role_mutation(user_ids: Union[ID, List[ID]], new_role: Union[BaseRoleName, str],
                               with_complexity: bool = False) -> str:
    """
    Construct a mutation to update a user's role. For more information, visit
    https://developer.monday.com/api-reference/reference/users#update-a-users-role

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
        new_role (Union[BaseRoleName, str]): The user's updated role.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    if isinstance(new_role, BaseRoleName):
        role = new_role.value
    elif isinstance(new_role, str):
        role = new_role
    else:
        raise ValueError("role must be of type BaseRoleName or str")

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_users_role (
            user_ids: {format_param_value(user_ids)}, new_role: {role}
        ) {{
            updated_users {{
                id
                name
                is_admin
                is_guest
                is_view_only
            }}
            errors {{
                message
                code 
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def deactivate_users_mutation(user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> str:
    """
    Construct a mutation to deactivate users from a monday.com account. For more information, visit
    https://developer.monday.com/api-reference/reference/users#deactivate-users

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to deactivate. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        deactivate_users (user_ids: {format_param_value(user_ids)}) {{
            deactivated_users {{
                id
                name
            }}
            errors {{
                message
                code 
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def activate_users_mutation(user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> str:
    """
    Construct a mutation to re-activates users in a monday.com account. For more information, visit
    https://developer.monday.com/api-reference/reference/users#activate-users

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to activate. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        activate_users (user_ids: {format_param_value(user_ids)}) {{
            activated_users {{
                id
                name
            }}
            errors {{
                message
                code 
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def update_users_email_domain_mutation(new_domain: str, user_ids: Union[ID, List[ID]],
                                       with_complexity: bool = False) -> str:
    """
    Construct a mutation to update a user's email domain. For more information, visit
    https://developer.monday.com/api-reference/reference/users#update-a-users-email-domain
    Args:
        new_domain (str): The updated email domain.
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_email_domain (
            input: {{
                new_domain: {format_param_value(new_domain)}, user_ids: {format_param_value(user_ids)}
            }}) {{
            updated_users {{
                id
                name
                email
            }}
            errors {{
                message
                code 
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = [
    "get_me_query",
    "get_users_query",
    "get_users_by_email_query",
    "deactivate_users_mutation",
    "activate_users_mutation",
    "update_users_email_domain_mutation",
    "update_users_role_mutation"
]
