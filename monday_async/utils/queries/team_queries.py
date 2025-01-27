from typing import List, Union

from monday_async.types import ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def get_teams_query(team_ids: Union[ID, List[ID]] = None, with_complexity: bool = False) -> str:
    """
    Construct a query to get all teams or get teams by ids if provided. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#queries

    Args:
        team_ids (Union[int, str, List[Union[int, str]]]):
            A single team ID, a list of team IDs, or None to get all teams.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        teams (ids: {format_param_value(team_ids if team_ids else None)}) {{
            id
            name
            users {{
                id
                email
                name
            }}
        }}
    }}
    """
    return graphql_parse(query)


def add_users_to_team_query(team_id: ID, user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> str:
    """
    Construct a query to add users to a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#add-users-to-a-team

    Args:
        team_id (Union[int, str]): The unique identifier of the team to add users to.

        user_ids (Union[int, str, List[Union[int, str]]]): A single user ID of a user or a list of user IDs.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        add_users_to_team (
            team_id: {format_param_value(team_id)},
            user_ids: {format_param_value(user_ids)}
        ) {{
            successful_users {{
                name
                email
             }}
            failed_users {{
                name
                email
            }}
        }}
    }}
    """
    return graphql_parse(query)


def remove_users_from_team_query(team_id: ID, user_ids: Union[ID, List[ID]], with_complexity: bool = False) -> str:
    """
    Construct a query to remove users from a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#remove-users-from-a-team

    Args:
        team_id (Union[int, str]): The unique identifier of the team to remove users from.

        user_ids (Union[int, str, List[Union[int, str]]]): A single user ID of a user or a list of user IDs.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        remove_users_from_team (
            team_id: {format_param_value(team_id)},
            user_ids: {format_param_value(user_ids)}
        ) {{
            successful_users {{
                name
                email
             }}
            failed_users {{
                name
                email
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_teams_query',
    'add_users_to_team_query',
    'remove_users_from_team_query'
]
