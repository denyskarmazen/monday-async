from typing import List, Union

from monday_async.types import UserKind, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def get_me_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get data about the user connected to the API key that is used. For more information, visit
    https://developer.monday.com/api-reference/reference/me#queries

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
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


__all__ = [
    "get_me_query",
    "get_users_query",
    "get_users_by_email_query"
]