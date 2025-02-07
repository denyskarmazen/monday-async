from typing import List, Union, Optional

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
                is_guest
            }}
            owners {{
                id
                name
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_team_query(name: str,
                      subscriber_ids: Optional[List[ID]] = None,
                      parent_team_id: Optional[ID] = None,
                      is_quest_team: bool = False,
                      allow_empty_teams: bool = True,
                      with_complexity: bool = False) -> str:
    """
    Construct a query to create to a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#create-team

    Args:
        name (str): The name of the team.
        subscriber_ids (Optional[List[ID]]): The unique identifiers of the subscribers to the team.
            Can be empty if allow_empty_teams is set to True.
        parent_team_id (Optional): The unique identifier of the parent team.
        is_quest_team (bool): Whether the team is a quest team.
        allow_empty_teams (bool): Whether to allow empty teams. True by default.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_team (
            input: {{
                name: {format_param_value(name)},
                is_guest_team: {format_param_value(is_quest_team)},
                parent_team_id: {format_param_value(parent_team_id)},
                subscriber_ids: {format_param_value(subscriber_ids)}
            }}
            options: {{ allow_empty_team: {format_param_value(allow_empty_teams)} }}
        ) {{
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


def delete_team_query(team_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to delete a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#delete-team
    Returns:
        team_id (Union[int, str, List[Union[int, str]]]): A single team ID of a team or a list of team IDs.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_team (team_id: {team_id}) {{
            id
            name
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
                id
                name
                email
             }}
            failed_users {{
                idd
                name
                email
            }}
        }}
    }}
    """
    return graphql_parse(query)


def assign_team_owners_query(user_ids: Union[ID, List[ID]], team_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to assign owners to a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#assign-team-owners

    Args:
        user_ids (Union[ID, List[ID]]): A single user ID of a user or a list of user IDs.
        team_id (ID): The unique identifier of the team to assign owners to.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        assign_team_owners (
            user_ids: {format_param_value(user_ids)},
            team_id: {format_param_value(team_id)}
        ) {{
            errors {{
                message
                code
                user_id
            }}
            team {{
                owners {{
                    id
                    name
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def remove_team_owners_query(user_ids: Union[ID, List[ID]], team_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to remove owners from a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#remove-team-owners

    Args:
        user_ids (Union[ID, List[ID]]): A single user ID of a user or a list of user IDs.
        team_id (ID): The unique identifier of the team to assign owners to.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        remove_team_owners (
            user_ids: {format_param_value(user_ids)},
            team_id: {format_param_value(team_id)}
        ) {{
            errors {{
                message
                code
                user_id
            }}
            team {{
                owners {{
                    id
                    name
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_teams_query',
    'create_team_query',
    'delete_team_query',
    'add_users_to_team_query',
    'remove_users_from_team_query',
    'assign_team_owners_query',
    'remove_team_owners_query'
]
