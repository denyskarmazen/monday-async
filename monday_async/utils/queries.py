import json
import re
from enum import Enum
from typing import List, Pattern, Union, Optional, Mapping, Any
from monday_async.utils.types import WebhookEventType, TargetType, UserKind, WorkspaceKind, State
from monday_async.utils.utils import monday_json_stringify, format_param_value, graphql_parse, gather_params


# ### COMPLEXITY RESOURCE QUERIES ### #
def add_complexity() -> str:
    """This can be added to any query to return its complexity with it"""
    query = f"""
        complexity {{
            before
            query
            after
            reset_in_x_seconds
        }}
    """
    return query


# ### API RESOURCE QUERIES ### #
def get_current_api_version_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get the api version used to make the request. For more information, visit
    https://developer.monday.com/api-reference/reference/version

    Parameters:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        version {{
            kind
            value
        }}
    }}
    """

    return graphql_parse(query)


def get_all_api_versions_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get all the monday.com api versions available. For more information, visit
    https://developer.monday.com/api-reference/reference/versions

    Parameters:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        versions {{
            kind
            value
        }}
    }}
    """

    return graphql_parse(query)


# ### WEBHOOK RESOURCE QUERIES ### #
def get_webhooks_by_board_id_query(board_id: Union[int, str], with_complexity: bool = False) -> str:
    """
    Construct a query to get all webhooks for a board. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#queries

    Parameters:
        board_id (Union[int, str]): a unique identifier of a board, can be an integer or
                                    a string containing integers.

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        webhooks(board_id: {format_param_value(board_id)}){{
            id
            event
            board_id
            config
        }}
    }}
    """

    return graphql_parse(query)


def create_webhook_query(board_id: Union[int, str], url: str, event: WebhookEventType, config: Optional[dict] = None,
                         with_complexity: bool = False) -> str:
    """
    Construct a query to create a webhook. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#create-a-webhook

    Parameters:
        board_id (Union[int, str]): a unique identifier of a board, can be an integer or
                                    a string containing integers.

        url (str): the webhook URL.

        event (WebhookEventType): the event type to listen to.

        config (dict): the webhook configuration, check https://developer.monday.com/api-reference/reference/webhooks
        for more info.

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    event_value = event.value if isinstance(event, WebhookEventType) else event

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_webhook (
            board_id: {format_param_value(board_id)},
            url: {format_param_value(url)}, 
            event: {event_value}, 
            config: {monday_json_stringify(config)}
        ) {{
            id
            board_id
            event
            config
        }}
    }}
    """

    return graphql_parse(query)


def delete_webhook_query(webhook_id: Union[int, str], with_complexity: bool = False) -> str:
    """
    Construct a query to delete a webhook connection. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

    Parameters:
        webhook_id (Union[int, str]): a unique identifier of a webhook, can be an integer or
                                    a string containing integers.

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_webhook (id: {format_param_value(webhook_id)}) {{
            id
            board_id
        }}
    }}
    """

    return graphql_parse(query)


# ### NOTIFICATION RESOURCE QUERIES ### #
def create_notification_query(user_id: Union[int, str], target_id: Union[int, str], text: str,
                              target_type: TargetType, with_complexity: bool = False) -> str:
    """
    Construct a query to create a notification. For more information, visit
    https://developer.monday.com/api-reference/reference/notification

    Parameters:
        user_id (Union[int, str]): the user's unique identifier.

        target_id (Union[int, str]): the target's unique identifier. The value depends on the target_type:
            - Project: the relevant item or board ID
            - Post : the relevant update or reply ID

        text (str): the notification's text.

        target_type (TargetType): the target's type: project or post.
            - Project: sends a notification referring to a specific item or board
            - Post : sends a notification referring to a specific item's update or reply

        with_complexity (bool): returns the complexity of the query with the query if set to True.

    """
    target_type_value = target_type.value if isinstance(target_type, TargetType) else target_type
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_notification (
            user_id: {format_param_value(user_id)}, 
            target_id: {format_param_value(target_id)}, 
            text: {format_param_value(text)}, 
            target_type: {target_type_value}
        ) {{
            text
        }}
    }}
    """

    return graphql_parse(query)


# ### USER RESOURCE QUERIES ### #
def get_me_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get data about the user connected to the API key that is used. For more information, visit
    https://developer.monday.com/api-reference/reference/me#queries

    Parameters:
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


def get_users_query(user_ids: Union[int, str, List[Union[int, str]]] = None, limit: int = 50,
                    user_kind: UserKind = UserKind.ALL, newest_first: bool = False,
                    page: int = 1, with_complexity: bool = False) -> str:
    """
    Construct a query to get all users or get users by ids if provided. For more information, visit
    https://developer.monday.com/api-reference/reference/users#queries

    Parameters:
        user_ids (Union[int, str, List[Union[int, str]]]): A single user ID, a list of user IDs, or None to get all users.

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

    Parameters:
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


def get_teams_query(team_ids: Union[int, str, List[Union[int, str]]] = None, with_complexity: bool = False) -> str:
    """
    Construct a query to get all teams or get teams by ids if provided. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#queries

    Parameters:
        team_ids (Union[int, str, List[Union[int, str]]]): A single team ID, a list of team IDs, or None to get all teams.

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


def add_users_to_team_query(team_id: Union[int, str], user_ids: Union[int, str, List[Union[int, str]]],
                            with_complexity: bool = False) -> str:
    """
    Construct a query to add users to a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#add-users-to-a-team

    Parameters:
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


def remove_users_from_team_query(team_id: Union[int, str], user_ids: Union[int, str, List[Union[int, str]]],
                                 with_complexity: bool = False) -> str:
    """
    Construct a query to remove users from a team. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#remove-users-from-a-team

    Parameters:
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


# ### WORKSPACE RESOURCE QUERIES ### #
def get_workspaces_query(workspace_ids: Union[int, str, List[Union[int, str]]] = None, limit: int = 25, page: int = 1,
                         kind: Optional[WorkspaceKind] = None, with_complexity: bool = False,
                         state: State = State.ACTIVE) -> str:
    """
    Construct a query to get workspaces. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#queries

    Parameters:
        workspace_ids (Union[int, str, List[Union[int, str]]]): A single workspace ID, a list of workspace IDs, or
        None to get all workspaces.

        limit (int): The number of workspaces to return. The default is 25.

        page (int): The page number to get. Starts at 1.

        kind (WorkspaceKind): The kind of workspaces to return: open or closed.

        state (State): The state of workspaces you want to search by: all, active, archived, or deleted.
        The default is active.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    if workspace_ids and isinstance(workspace_ids, list):
        limit = len(workspace_ids)

    if kind:
        workspace_kind_value = kind.value if isinstance(kind, WorkspaceKind) else kind
    else:
        workspace_kind_value = "null"

    state_value = state.value if isinstance(state, State) else state

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        workspaces (
            ids: {format_param_value(workspace_ids if workspace_ids else None)},
            kind: {workspace_kind_value},
            limit: {limit},
            page: {page},
            state: {state_value}
            
        ) {{
            id
            name
            kind
            description
            state
        }}
    }}
    """

    return graphql_parse(query)


def create_workspace_query(name: str, kind: WorkspaceKind, description: Optional[str] = None,
                           with_complexity: bool = False):
    """
    Construct a query to create a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#create-a-workspace

    Parameters:
        name (str): The new workspace's name.

        kind (WorkspaceKind): The new workspace's kind: open or closed.

        description (Optional[str]): The new workspace's description.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    workspace_kind_value = kind.value if isinstance(kind, WorkspaceKind) else kind
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_workspace (
            name:{format_param_value(name)}, 
            kind: {workspace_kind_value}, 
            description: {format_param_value(description)}
        ) {{
            id
            name
            description
            kind
        }}
    }}
    """

    return graphql_parse(query)


def update_workspace_query(workspace_id: Union[int, str], name: Optional[str] = None,
                           kind: Optional[WorkspaceKind] = None, description: Optional[str] = None,
                           with_complexity: bool = False):
    """
    Construct a query to update a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#update-a-workspace

    Parameters:
        workspace_id (Union[int, str]): The unique identifier of the workspace to update.


        name (str): The updated workspace name.

        kind (WorkspaceKind): The kind of workspace to update: open or closed.

        description (Optional[str]): The updated workspace description.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    raw_params = locals().items()
    update_params = gather_params(raw_params, excluded_params=["workspace_id", "with_complexity"])

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_workspace (
            id: {format_param_value(workspace_id)},
            attributes: {{{update_params}}}
        ) {{
            id
            name
            description
            kind
        }}
    }}
    """

    return graphql_parse(query)


def delete_workspace_query(workspace_id, with_complexity: bool = False):
    """
    Construct a query to delete a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-a-workspace

    Parameters:
        workspace_id (Union[int, str]): The unique identifier of the workspace to update.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """


# ### FOLDER RESOURCE QUERIES ### #

# ### BOARD RESOURCE QUERIES ### #

# ### TAG RESOURCE QUERIES ### #

# ### COLUMN RESOURCE QUERIES ### #

# ### GROUP RESOURCE QUERIES### #

# ### ITEM RESOURCE QUERIES ### #

# ### UPDATE RESOURCE QUERIES ### #


# ### TESTING ### #
board = 6282896797


def query_tester(query):
    print(query)
    return query

