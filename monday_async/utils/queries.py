from enum import Enum
from typing import List, Union, Optional, Any

from monday_async.query_params import QueryParams, ItemByColumnValuesParam
from monday_async.types import (WebhookEventType, TargetType, UserKind, WorkspaceKind, State,
                                FolderColor, SubscriberKind, BoardKind, BoardAttributes, GroupUpdateColors,
                                DuplicateBoardType, PositionRelative, ColumnType, BoardsOrderBy, GroupAttributes,
                                GroupColors)
from monday_async.utils.utils import (monday_json_stringify, format_param_value, graphql_parse, gather_params,
                                      format_dict_value)

ID = Union[int, str]


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


def add_column_values() -> str:
    column_values = f"""
    column_values {{
        id
        column {{
            title
            settings_str
        }}
        type
        text
        value
        ... on BoardRelationValue {{
            display_value
            linked_item_ids
        }}
        ... on CheckboxValue {{
            checked
        }}
        ... on CountryValue {{
            country {{
                name 
            }}
        }}
        ... on DateValue {{
            date
            time
        }}
        ... on LocationValue {{
            lat
            lng
            address
        }}
        ... on MirrorValue {{
            display_value
            mirrored_items {{
                linked_item {{
                    id
                    name
                }}
            }}
        }}
        ... on PeopleValue {{
            persons_and_teams {{
                id
                kind
            }}
        }}
    }}   
    """
    return column_values


def add_subitems() -> str:
    subitems = f"""
    subitems {{
        id
        name
        url
        state
    }}
    """
    return subitems


def add_updates() -> str:
    updates = f"""
    updates (limit: 100) {{
        id
        text_body
        body
        creator_id
        assets {{
            id 
            name
            file_extension
            url
            public_url 
        }}
        replies {{
            id
            text_body
        }}
    }}
    """
    return updates


# ### COMPLEXITY RESOURCE QUERIES ### #
def get_complexity_query() -> str:
    """
    Construct a query to get the current complexity points. For more information visit
    https://developer.monday.com/api-reference/reference/complexity
    """

    query = f"""query {{{add_complexity()}}}"""
    return graphql_parse(query)


# ### API RESOURCE QUERIES ### #
def get_current_api_version_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get the api version used to make the request. For more information, visit
    https://developer.monday.com/api-reference/reference/version

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        version {{
            display_name
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

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        versions {{
            display_name
            kind
            value
        }}
    }}
    """
    return graphql_parse(query)


# ### WEBHOOK RESOURCE QUERIES ### #
def get_webhooks_by_board_id_query(board_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to get all webhooks for a board. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#queries

    Args:
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


def create_webhook_query(board_id: ID, url: str, event: WebhookEventType, config: Optional[dict] = None,
                         with_complexity: bool = False) -> str:
    """
    Construct a query to create a webhook. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#create-a-webhook

    Args:
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


def delete_webhook_query(webhook_id: ID, with_complexity: bool = False) -> str:
    """
    Construct a query to delete a webhook connection. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#delete-a-webhook

    Args:
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
def create_notification_query(user_id: ID, target_id: ID, text: str, target_type: TargetType,
                              with_complexity: bool = False) -> str:
    """
    Construct a query to create a notification. For more information, visit
    https://developer.monday.com/api-reference/reference/notification

    Args:
        user_id (ID): the user's unique identifier.
        target_id (ID): the target's unique identifier. The value depends on the target_type:
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


# ### WORKSPACE RESOURCE QUERIES ### #
def get_workspaces_query(workspace_ids: Union[ID, List[ID]] = None, limit: int = 25, page: int = 1,
                         kind: Optional[WorkspaceKind] = None, with_complexity: bool = False,
                         state: State = State.ACTIVE) -> str:
    """
    Construct a query to get workspaces. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#queries

    Args:
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

    Args:
        name (str): The new workspace name.

        kind (WorkspaceKind): The new workspace kind: open or closed.

        description (Optional[str]): The new workspace description.

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


def update_workspace_query(workspace_id: ID, name: Optional[str] = None, kind: Optional[WorkspaceKind] = None,
                           description: Optional[str] = None, with_complexity: bool = False):
    """
    Construct a query to update a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#update-a-workspace

    Args:
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


def delete_workspace_query(workspace_id: Union[int, str], with_complexity: bool = False):
    """
    Construct a query to delete a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-a-workspace

    Args:
        workspace_id (Union[int, str]): The unique identifier of the workspace to delete.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_workspace (workspace_id: {workspace_id}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def add_users_to_workspace_query(workspace_id: ID, user_ids: Union[ID, List[ID]],
                                 kind: SubscriberKind, with_complexity: bool = False) -> str:
    """
    This query adds users as subscribers or owners to a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#add-users-to-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to add to the workspace.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        add_users_to_workspace (
            workspace_id: {format_param_value(workspace_id)},
            user_ids: {format_param_value(user_ids)},
            kind: {kind_value}
        ) {{
            id
            name
            email
        }}
    }}
    """
    return graphql_parse(query)


def delete_users_from_workspace_query(workspace_id: ID, user_ids: Union[ID, List[ID]],
                                      with_complexity: bool = False) -> str:
    """
    This query removes users from a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-users-from-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to remove from the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_users_from_workspace (
            workspace_id: {format_param_value(workspace_id)},
            user_ids: {format_param_value(user_ids)}
        ) {{
            id
            name
            email
        }}
    }}
    """
    return graphql_parse(query)


def add_teams_to_workspace_query(workspace_id: ID, team_ids: Union[ID, List[ID]],
                                 kind: SubscriberKind, with_complexity: bool = False) -> str:
    """
    This query adds teams as subscribers or owners to a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#add-teams-to-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to add to the workspace.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        add_teams_to_workspace (
            workspace_id: {format_param_value(workspace_id)},
            team_ids: {format_param_value(team_ids)},
            kind: {kind_value}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def delete_teams_from_workspace_query(workspace_id: ID, team_ids: Union[ID, List[ID]],
                                      with_complexity: bool = False) -> str:
    """
    This query removes teams from a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-teams-from-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to remove from the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_teams_from_workspace (
            workspace_id: {format_param_value(workspace_id)},
            team_ids: {format_param_value(team_ids)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


# ### FOLDER RESOURCE QUERIES ### #
def get_folders_query(ids: Union[ID, List[ID]] = None, workspace_ids: Union[ID, List[ID]] = None,
                      limit: int = 25, page: int = 1, with_complexity: bool = False) -> str:
    """
    This query retrieves folders, allowing you to specify specific folders, workspaces, limits, and pagination.
    For more information, visit https://developer.monday.com/api-reference/reference/folders#queries
    Args:
        ids (Union[ID, List[ID]]): (Optional) A single folder ID or a list of IDs to retrieve specific folders.

        workspace_ids (Union[ID, List[ID]]): (Optional) A single workspace ID or a list of IDs to filter folders
            by workspace. Use null to include the Main Workspace.

        limit (int): (Optional) The maximum number of folders to return. Default is 25, maximum is 100.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        folders (
            ids: {format_param_value(ids if ids else None)},
            workspace_ids: {format_param_value(workspace_ids if workspace_ids else None)},
            limit: {limit},
            page: {page}
        ) {{
            id
            name
            color
            parent {{
                id
                name
            }}
            sub_folders {{
                id
                name
            }}
            workspace {{
                id
                name
            }}

        }}
    }}
    """
    return graphql_parse(query)


def create_folder_query(workspace_id: ID, name: str, color: Optional[FolderColor] = FolderColor.NULL,
                        parent_folder_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new folder within a specified workspace and parent folder (optional).
    For more information, visit https://developer.monday.com/api-reference/reference/folders#create-a-folder

    Args:
        workspace_id (ID): The unique identifier of the workspace where the folder will be created.

        name (str): The name of the new folder.

        color (FolderColor): (Optional) The color of the new folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the parent folder within the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    color_value = color.value if isinstance(color, FolderColor) else color

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_folder (
            workspace_id: {format_param_value(workspace_id)},
            name: {format_param_value(name)},
            color: {color_value},
            parent_folder_id: {format_param_value(parent_folder_id)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


def update_folder_query(folder_id: ID, name: Optional[str] = None, color: Optional[FolderColor] = None,
                        parent_folder_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query modifies an existing folder's name, color, or parent folder.

    Args:
        folder_id (ID): The unique identifier of the folder to update.

        name (str): (Optional) The new name for the folder.

        color (FolderColor): (Optional) The new color for the folder, chosen from the FolderColor enum.

        parent_folder_id (ID): (Optional) The ID of the new parent folder for the folder.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    raw_params = locals().items()
    update_params = gather_params(raw_params, excluded_params=["folder_id", "with_complexity"])

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_folder (
            folder_id: {format_param_value(folder_id)},
            {update_params}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


def delete_folder_query(folder_id: ID, with_complexity: bool = False) -> str:
    """
    This query permanently removes a folder from a workspace.

    Args:
        folder_id (ID): The unique identifier of the folder to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_folder (folder_id: {format_param_value(folder_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


# ### BOARD RESOURCE QUERIES ### #
def get_boards_query(ids: Union[ID, List[ID]] = None, board_kind: Optional[BoardKind] = None,
                     state: State = State.ACTIVE, workspace_ids: Union[ID, List[ID]] = None,
                     order_by: Optional[BoardsOrderBy] = None, limit: int = 25, page: int = 1,
                     with_complexity: bool = False) -> str:
    """
    This query retrieves boards, offering filtering by IDs, board kind, state, workspace, and ordering options.
    For more information, visit https://developer.monday.com/api-reference/reference/boards#queries

    Args:
        ids (List[ID]): (Optional) A list of board IDs to retrieve specific boards.

        board_kind (BoardKind): (Optional) The kind of boards to retrieve: public, private, or share.

        state (State): (Optional) The state of the boards: all, active, archived, or deleted. Defaults to active.

        workspace_ids (Union[ID, List[ID]]): (Optional) A list of workspace IDs or a single
            workspace ID to filter boards by specific workspaces.

        order_by (BoardsOrderBy): (Optional) The property to order the results by: created_at or used_at.

        limit (int): (Optional) The maximum number of boards to return. Defaults to 25.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    state_value = state.value if isinstance(state, State) else state

    if ids and isinstance(ids, list):
        limit = len(ids)
    if board_kind:
        board_kind_value = board_kind.value if isinstance(board_kind, BoardKind) else board_kind
    else:
        board_kind_value = "null"

    if order_by:
        order_by_value = order_by.value if isinstance(order_by, BoardsOrderBy) else order_by
    else:
        order_by_value = "null"

    workspace_ids_value = f"workspace_ids: {format_param_value(workspace_ids)}" if workspace_ids else ""
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (
            ids: {format_param_value(ids if ids else None)},
            board_kind: {board_kind_value},
            state: {state_value},
            {workspace_ids_value}
            order_by: {order_by_value},
            limit: {limit},
            page: {page}
        ) {{
            id
            name
            board_kind
            state
            workspace_id
            description
            groups {{
                id
                title
                color
            }}
            columns {{
                id
                title
                type
            }}
            item_terminology
                subscribers {{
                name
                id
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_board_query(board_name: str, board_kind: BoardKind, description: Optional[str] = None,
                       folder_id: Optional[ID] = None, workspace_id: Optional[ID] = None,
                       template_id: Optional[ID] = None, board_owner_ids: List[ID] = None,
                       board_owner_team_ids: List[ID] = None, board_subscriber_ids: List[ID] = None,
                       board_subscriber_teams_ids: List[ID] = None, empty: bool = False,
                       with_complexity: bool = False) -> str:
    """
    This query creates a new board with specified name, kind, and optional description, folder, workspace, template,
    and subscribers/owners.
    For more information, visit https://developer.monday.com/api-reference/reference/boards#create-a-board

    Args:
        board_name (str): The name of the new board.

        board_kind (BoardKind): The kind of board to create: public, private, or share.

        description (str): (Optional) A description for the new board.

        folder_id (ID): (Optional) The ID of the folder to create the board in.

        workspace_id (ID): (Optional) The ID of the workspace to create the board in.

        template_id (ID): (Optional) The ID of a board template to use for the new board's structure.

        board_owner_ids (List[ID]): (Optional) A list of user IDs to assign as board owners.

        board_owner_team_ids (List[ID]): (Optional) A list of team IDs to assign as board owners.

        board_subscriber_ids (List[ID]): (Optional) A list of user IDs to subscribe to the board.

        board_subscriber_teams_ids (List[ID]): (Optional) A list of team IDs to subscribe to the board.

        empty (bool): (Optional) Set to True to create an empty board without default items. Defaults to False.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    board_kind_value = board_kind.value if isinstance(board_kind, BoardKind) else board_kind
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_board (
            board_name: {format_param_value(board_name)},
            board_kind: {board_kind_value},
            description: {format_param_value(description)},
            folder_id: {format_param_value(folder_id)},
            workspace_id: {format_param_value(workspace_id)},
            template_id: {format_param_value(template_id)},
            board_owner_ids: {format_param_value(board_owner_ids)},
            board_owner_team_ids: {format_param_value(board_owner_team_ids)},
            board_subscriber_ids: {format_param_value(board_subscriber_ids)},
            board_subscriber_teams_ids: {format_param_value(board_subscriber_teams_ids)},
            empty: {format_param_value(empty)}
        ) {{
            id
            name
            board_kind
        }}
    }}
    """
    return graphql_parse(query)


def duplicate_board_query(board_id: ID, duplicate_type: DuplicateBoardType,
                          board_name: Optional[str] = None, workspace_id: Optional[ID] = None,
                          folder_id: Optional[ID] = None, keep_subscribers: bool = False,
                          with_complexity: bool = False) -> str:
    """
    This query duplicates a board with options to include structure, items, updates, and subscribers.
    For more information, visit https://developer.monday.com/api-reference/reference/boards#duplicate-a-board

    Args:
        board_id (ID): The ID of the board to duplicate.

        duplicate_type (DuplicateBoardType): The type of duplication: duplicate_board_with_structure,

        duplicate_board_with_pulses, or duplicate_board_with_pulses_and_updates.

        board_name (str): (Optional) The name for the new duplicated board.
            If omitted, a name is automatically generated.

        workspace_id (ID): (Optional) The ID of the workspace to place the duplicated board in.
            Defaults to the original board's workspace.

        folder_id (ID): (Optional) The ID of the folder to place the duplicated board in.
            Defaults to the original board's folder.

        keep_subscribers (bool): (Optional) Whether to copy subscribers to the new board. Defaults to False.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    duplicate_type_value = duplicate_type.value if isinstance(duplicate_type, DuplicateBoardType) else duplicate_type

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        duplicate_board (
            board_id: {format_param_value(board_id)},
            duplicate_type: {duplicate_type_value},
            board_name: {format_param_value(board_name)},
            workspace_id: {format_param_value(workspace_id)},
            folder_id: {format_param_value(folder_id)},
            keep_subscribers: {format_param_value(keep_subscribers)}
        ) {{
            board {{
                id
                name
            }}
        }}
    }}
    """
    return graphql_parse(query)


def update_board_query(board_id: ID, board_attribute: BoardAttributes, new_value: str,
                       with_complexity: bool = False) -> str:
    """
    This query updates a board attribute. For more information, visit
    https://developer.monday.com/api-reference/reference/boards#update-a-board

    Args:
        board_id (ID): The ID of a board to update

        board_attribute (BoardAttributes): The board's attribute to update: name, description, or communication.

        new_value (str): The new attribute value

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    board_attribute_value = board_attribute.value if isinstance(board_attribute, BoardAttributes) else board_attribute
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_board (
            board_id: {format_param_value(board_id)},
            board_attribute: {board_attribute_value},
            new_value: {format_param_value(new_value)}
        )
    }}
    """
    return graphql_parse(query)


def archive_board_query(board_id: ID, with_complexity: bool = False) -> str:
    """
    This query archives a board, making it no longer visible in the active board list. For more information, visit
    https://developer.monday.com/api-reference/reference/boards#archive-a-board

    Args:
        board_id (ID): The ID of the board to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_board (board_id: {format_param_value(board_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def delete_board_query(board_id: ID, with_complexity: bool = False) -> str:
    """
    This query permanently deletes a board. For more information, visit
    https://developer.monday.com/api-reference/reference/boards#delete-a-board

    Args:
        board_id (ID): The ID of the board to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_board (board_id: {format_param_value(board_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def add_users_to_board_query(board_id: ID, user_ids: Union[ID, List[ID]], kind: SubscriberKind,
                             with_complexity: bool = False) -> str:
    """
    This query adds users as subscribers or owners to a board. For more information, visit
    https://developer.monday.com/api-reference/reference/users#add-users-to-a-board

    Args:
        board_id (ID): The ID of the board to add users to.

        user_ids (Union[ID, List[ID]]): A list of user IDs to add as subscribers or owners.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind

    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        add_users_to_board (
            board_id: {format_param_value(board_id)},
            user_ids: {format_param_value(user_ids)},
            kind: {kind_value}
        ) {{
            id
            name
            email
        }}
    }}
    """
    return graphql_parse(query)


def remove_users_from_board_query(board_id: ID, user_ids: Union[ID, List[ID]],
                                  with_complexity: bool = False) -> str:
    """
    This query removes users from a board's subscribers or owners. For more information, visit
    https://developer.monday.com/api-reference/reference/users#delete-subscribers-from-a-board

    Args:
        board_id (ID): The ID of the board to remove users from.

        user_ids (Union[ID, List[ID]]): A list of user IDs to remove from the board.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_subscribers_from_board (
            board_id: {format_param_value(board_id)},
            user_ids: {format_param_value(user_ids)}
        ) {{
            id
            name
            email
        }}
    }}
    """
    return graphql_parse(query)


def add_teams_to_board_query(board_id: ID, team_ids: Union[ID, List[ID]], kind: SubscriberKind,
                             with_complexity: bool = False) -> str:
    """
    This query adds teams as subscribers or owners to a board. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#add-teams-to-a-board

    Args:
        board_id (ID): The ID of the board to add teams to.

        team_ids (Union[ID, List[ID]]): A list of team IDs to add as subscribers or owners.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        add_teams_to_board (
            board_id: {format_param_value(board_id)},
            team_ids: {format_param_value(team_ids)},
            kind: {kind_value}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def delete_teams_from_board_query(board_id: ID, team_ids: Union[ID, List[ID]],
                                  with_complexity: bool = False) -> str:
    """
    This query removes teams from a board's subscribers or owners. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#delete-teams-from-a-board

    Args:
        board_id (ID): The ID of the board to remove teams from.

        team_ids (Union[ID, List[ID]]): A list of team IDs to remove from the board.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_teams_from_board (
            board_id: {format_param_value(board_id)},
            team_ids: {format_param_value(team_ids)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def get_board_views_query(board_id: ID, ids: Union[ID, List[ID]] = None, view_type: Optional[str] = None,
                          with_complexity: bool = False) -> str:
    """
    This query retrieves the views associated with a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/board-views#queries

    Args:
        board_id (ID): The ID of the board to retrieve views from.

        ids (Union[ID, List[ID]]): (Optional) A list of view IDs to retrieve specific views.

        view_type (str): (Optional) The type of views to retrieve.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            views (ids: {format_param_value(ids if ids else None)}, type: {format_param_value(view_type)}) {{
                type
                settings_str
                view_specific_data_str
                name
                id
            }}
        }}
    }}
    """
    return graphql_parse(query)


# ### TAG RESOURCE QUERIES ### #
def get_tags_query(ids: Union[ID, List[ID]] = None, with_complexity: bool = False) -> str:
    """
    This query retrieves tags, allowing you to specify individual tags or retrieve all tags. For more information, visit
    https://developer.monday.com/api-reference/reference/tags-1#queries

    Args:
        ids (Union[ID, List[ID]]): (Optional) A list of tag IDs to retrieve specific tags.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        tags (ids: {format_param_value(ids if ids else None)}) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


def get_tags_by_board_query(board_id: ID, with_complexity: bool = False) -> str:
    """
    This query retrieves tags associated with a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/tags-1#queries

    Args:
        board_id (ID): The ID of the board to retrieve tags from.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            tags {{
                id
                name
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_or_get_tag_query(tag_name: str, board_id: Optional[ID] = None,
                            with_complexity: bool = False) -> str:
    """
    This query creates a new tag with the specified name or retrieves the existing tag if it already exists.
    For more information, visit https://developer.monday.com/api-reference/reference/tags-1#create-or-get-a-tag

    Args:
        tag_name (str): The name of the tag to create or retrieve.

        board_id (ID): (Optional) The ID of the private board to create the tag in. Not needed for public boards.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_or_get_tag (
            tag_name: {format_param_value(tag_name)},
            board_id: {format_param_value(board_id)}
        ) {{
            id
            name
            color
        }}
    }}
    """
    return graphql_parse(query)


# ### COLUMN RESOURCE QUERIES ### #
def get_columns_by_board_query(board_id: ID, ids: Union[ID, List[ID]] = None,
                               types: Union[ColumnType, List[ColumnType]] = None, with_complexity: bool = False) -> str:
    """
    This query retrieves columns associated with a specific board, allowing filtering by column IDs and types.
    For more information, visit https://developer.monday.com/api-reference/reference/columns#queries

    Args:
        board_id (ID): The ID of the board to retrieve columns from.

        ids (Union[ID, List[ID]]): (Optional) A list of column IDs to retrieve specific columns.

        types (List[ColumnType]): (Optional) A list of column types to filter by.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            id
            name
            columns (ids: {format_param_value(ids if ids else None)}, types: {format_param_value(types)}) {{
                id
                title
                type
                description
                settings_str
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_column_query(board_id: ID, title: str, column_type: ColumnType, description: Optional[str] = None,
                        defaults: Optional[dict] = None, column_id: Optional[str] = None,
                        after_column_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new column on a specific board with a specified title, type, and optional description,
    defaults, user-specified ID, and positioning.
    For more information, visit https://developer.monday.com/api-reference/reference/columns#create-a-column

    Args:
        board_id (ID): The ID of the board to create the column on.

        title (str): The title of the new column.

        column_type (ColumnType): The type of column to create, chosen from the ColumnType enum.

        description (str): (Optional) A description for the new column.

        defaults (dict): (Optional) The default value for the new column as a dictionary.

        column_id (str): (Optional) A user-specified unique identifier for the column. Has to meet requirements:
            - [1-20] characters in length (inclusive)
            - Only lowercase letters (a-z) and underscores (_)
            - Must be unique (no other column on the board can have the same ID)
            - Can't reuse column IDs, even if the column has been deleted from the board
            - Can't be null, blank, or an empty string

        after_column_id (ID): (Optional) The ID of the column after which to insert the new column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    column_type_value = column_type.value if isinstance(column_type, ColumnType) else column_type
    id_value = f"id: {format_param_value(column_id)}" if column_id else ""
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_column (
            board_id: {format_param_value(board_id)},
            title: {format_param_value(title)},
            column_type: {column_type_value},
            description: {format_param_value(description)},
            defaults: {monday_json_stringify(defaults)},
            after_column_id: {format_param_value(after_column_id)},
            {id_value}
        ) {{
            id
            title
            type
            description
        }}
    }}
    """
    return graphql_parse(query)


def change_column_title_query(board_id: ID, column_id: str, title: str,
                              with_complexity: bool = False) -> str:
    """
    This query updates the title of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-column-title

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        title (str): The new title for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_title (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)},
            title: {format_param_value(title)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(query)


def change_column_description_query(board_id: ID, column_id: str, description: str,
                                    with_complexity: bool = False) -> str:
    """
    This query updates the description of an existing column on a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-column-metadata

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to update.

        description (str): The new description for the column.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_metadata (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)},
            column_property: description,
            value: {format_param_value(description)}
        ) {{
            id
            description
        }}
    }}
    """
    return graphql_parse(query)


def delete_column_query(board_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This query removes a column from a specific board. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#delete-a-column

    Args:
        board_id (ID): The ID of the board containing the column.

        column_id (str): The unique identifier of the column to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_column (
            board_id: {format_param_value(board_id)},
            column_id: {format_param_value(column_id)}
        ) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


# ### GROUP RESOURCE QUERIES ### #
def get_groups_by_board_query(board_id: ID, ids: Union[str, List[str]] = None,
                              with_complexity: bool = False) -> str:
    """
    This query retrieves groups associated with a specific board, with the option to filter by group IDs.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#queries

    Args:
        board_id (ID): The ID of the board to retrieve groups from.

        ids (Union[ID, List[ID]]): (Optional) A list of group IDs to retrieve specific groups.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            groups (ids: {format_param_value(ids if ids else None)}) {{
                id
                title
                color
                position
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_group_query(board_id: ID, group_name: str, group_color: Optional[Union[GroupColors, str]] = None,
                       relative_to: Optional[str] = None, position_relative_method: Optional[PositionRelative] = None,
                       with_complexity: bool = False) -> str:
    """
    This query creates a new group on a specific board with a specified name and positioning relative to other groups.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#create-a-group

    Args:
        board_id (ID): The ID of the board to create the group on.

        group_name (str): The name of the new group.

        group_color (Optional[Union[GroupColors, str]]): The group's color. Pass as a HEX value when passing as a string
            For some reason currently not all colors work.

        relative_to (str): (Optional) The ID of the group to position the new group relative to.

        position_relative_method (PositionRelative): (Optional) The method for positioning the new group:
            before_at or after_at.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if position_relative_method:
        position_relative_method_value = position_relative_method.value \
            if isinstance(position_relative_method, PositionRelative) else position_relative_method
    else:
        position_relative_method_value = "null"

    group_color_value = group_color.value if isinstance(group_color, GroupColors) else group_color
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_group (
            board_id: {format_param_value(board_id)},
            group_name: {format_param_value(group_name)},
            group_color: {format_param_value(group_color_value)},
            relative_to: {format_param_value(relative_to)},
            position_relative_method: {position_relative_method_value}
        ) {{
            id
            title
            color
        }}
    }}
    """
    return graphql_parse(query)


def update_group_query(board_id: ID, group_id: str, group_attribute: GroupAttributes,
                       new_value: Union[Any, GroupUpdateColors], with_complexity: bool = False) -> str:
    """
    This query modifies an existing group's title, color, or position on the board.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#update-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to update.

        group_attribute (GroupAttributes): The attribute of the group to update: title, color,
            relative_position_after, or relative_position_before.

        new_value (str): The new value for the specified group attribute.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    group_attribute_value = group_attribute.value if isinstance(group_attribute, GroupAttributes) else group_attribute
    group_new_value = new_value.value if isinstance(new_value, Enum) else new_value
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            group_attribute: {group_attribute_value},
            new_value: {format_param_value(group_new_value)}
        ) {{
            id
            title
            color
            position
        }}
    }}
    """
    return graphql_parse(query)


def duplicate_group_query(board_id: ID, group_id: str, add_to_top: Optional[bool] = None,
                          group_title: Optional[str] = None, with_complexity: bool = False) -> str:
    """
    This query creates a copy of a group within the same board,
        with options to position the new group and set its title.
    For more information, visit https://developer.monday.com/api-reference/reference/groups#duplicate-group

    Args:
        board_id (ID): The ID of the board containing the group to duplicate.

        group_id (str): The unique identifier of the group to duplicate.

        add_to_top (bool): (Optional) Whether to add the new group to the top of the board.

        group_title (str): (Optional) The title for the new duplicated group.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        duplicate_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            add_to_top: {format_param_value(add_to_top)},
            group_title: {format_param_value(group_title)}
        ) {{
            id
            title
        }}
    }}
    """
    return graphql_parse(query)


def archive_group_query(board_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This query archives a group on a specific board, removing it from the active view. For more information, visit
    https://developer.monday.com/api-reference/reference/groups#archive-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def delete_group_query(board_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This query permanently removes a group from a board. For more information, visit
    https://developer.monday.com/api-reference/reference/groups#delete-a-group

    Args:
        board_id (ID): The ID of the board containing the group.

        group_id (str): The unique identifier of the group to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_group (
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


# ### ITEM RESOURCE QUERIES ### #
def get_items_by_id_query(ids: Union[ID, List[ID]], newest_first: Optional[bool] = None,
                          exclude_nonactive: Optional[bool] = None, limit: int = 25, page: int = 1,
                          with_complexity: bool = False, with_column_values: bool = True,
                          with_subitems: bool = False, with_updates: bool = False) -> str:
    """
    This query retrieves items, allowing filtering by IDs, sorting, and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items#queries

    Args:
        ids (Union[ID, List[ID]]):  A list of item IDs to retrieve specific items.

        newest_first (bool): (Optional) Set to True to order results with the most recently created items first.

        exclude_nonactive (bool): (Optional) Set to True to exclude inactive, deleted,
            or items belonging to deleted items.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (
            ids: {format_param_value(ids)},
            newest_first: {format_param_value(newest_first)},
            exclude_nonactive: {format_param_value(exclude_nonactive)},
            limit: {limit},
            page: {page}
        ) {{
            id
            name
            state
            {add_updates() if with_updates else ""}
            {add_column_values() if with_column_values else ""}
            {add_subitems() if with_subitems else ""}
            url
            group {{
                id
                title
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_board_query(board_ids: Union[ID, List[ID]], query_params: Optional[QueryParams] = None,
                             limit: int = 25, cursor: str = None, with_complexity: bool = False,
                             with_column_values: bool = True, with_subitems: bool = False,
                             with_updates: bool = False) -> str:
    """
    This query retrieves items from a specific board, allowing filtering by IDs, sorting, and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

    Args:
        board_ids (ID): The ID of the board to retrieve items from.

        query_params (QueryParams): (Optional) A set of parameters to filter, sort,
            and control the scope of the boards query. Use this to customize the results based on specific criteria.
            Please note that you can't use query_params and cursor in the same request.
            We recommend using query_params for the initial request and cursor for paginated requests.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    # If a cursor is provided setting query_params to None
    # since you cant use query_params and cursor in the same request.
    if cursor:
        query_params = None

    if query_params:
        query_params_value = f"query_params: {query_params}"
    else:
        query_params_value = ""

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_ids)}) {{
            items_page (
                limit: {limit},
                cursor: {format_param_value(cursor)},
                {query_params_value},
            ) {{
                cursor
                items {{
                    id
                    name
                    state
                    {add_updates() if with_updates else ""}
                    {add_column_values() if with_column_values else ""}
                    {add_subitems() if with_subitems else ""}
                    url
                    group {{
                        id
                        title
                        color
                    }}
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_group_query(board_id: ID, group_id: ID, query_params: Optional[QueryParams] = None,
                             limit: int = 25, cursor: str = None, with_complexity: bool = False,
                             with_column_values: bool = True, with_subitems: bool = False,
                             with_updates: bool = False) -> str:
    """
    This query retrieves items from a specific group within a board, allowing filtering by IDs, sorting,
    and excluding inactive items.
    For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

    Args:
        board_id (ID): The ID of the board to retrieve items from.

        group_id (ID): The ID of the group to get the items by

        query_params (QueryParams): (Optional) A set of parameters to filter, sort,
            and control the scope of the boards query. Use this to customize the results based on specific criteria.
            Please note that you can't use query_params and cursor in the same request.
            We recommend using query_params for the initial request and cursor for paginated requests.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    # If a cursor is provided setting query_params to None
    # since you cant use query_params and cursor in the same request.
    if cursor:
        query_params = None

    if query_params:
        query_params_value = f"query_params: {query_params}"
    else:
        query_params_value = ""

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        boards (ids: {format_param_value(board_id)}) {{
            groups (ids: {format_param_value(group_id)}) {{
                items_page (
                    limit: {limit},
                    cursor: {format_param_value(cursor)},
                    {query_params_value},
                ) {{
                    cursor
                    items {{
                        id
                        name
                        state
                        {add_updates() if with_updates else ""}
                        {add_column_values() if with_column_values else ""}
                        {add_subitems() if with_subitems else ""}
                        url
                    }}
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_column_value_query(board_id: ID, column_id: str, column_values: Union[str, List[str]], limit: int = 25,
                                    cursor: str = None, with_complexity: bool = False,
                                    with_column_values: bool = True, with_subitems: bool = False,
                                    with_updates: bool = False) -> str:
    """
    This query retrieves items based on the value of a specific column. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

    Args:
        board_id (ID): The ID of the board containing the items.

        column_id (str): The unique identifier of the column to filter by.

        column_values (Union[str, List[str]]): The column value to search for.

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    if cursor:
        columns_value = ""

    else:
        params = ItemByColumnValuesParam()
        params.add_column(column_id=column_id, column_values=column_values)
        columns_value = "columns: " + format_dict_value(params.value[0])

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items_page_by_column_values (
            board_id: {format_param_value(board_id)},
            limit: {limit},
            cursor: {format_param_value(cursor)},
            {columns_value}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_items_by_multiple_column_values_query(board_id: ID, columns: Union[ItemByColumnValuesParam, dict, List[dict]],
                                              limit: int = 25, cursor: str = None, with_complexity: bool = False,
                                              with_column_values: bool = True, with_subitems: bool = False,
                                              with_updates: bool = False) -> str:
    """
    This query retrieves items based on the value of a specific column. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

    Args:
        board_id (ID): The ID of the board containing the items.

        columns (Union[ItemByColumnValuesParam, dict]): The column values to filter by can be ItemByColumnValuesParam
            instance or a list consisting of dictionaries of this format:
            {"column_id": column_id, "column_values": column_values}

        limit (int): (Optional) The maximum number of items to return. Defaults to 25.

        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.
    """
    if cursor:
        columns_value = ""


    else:

        if isinstance(columns, ItemByColumnValuesParam):
            formatted_columns = [format_dict_value(column) for column in columns.value]
            columns_value = "columns: [" + ", ".join(formatted_columns) + "]"

        elif isinstance(columns, list):
            formatted_columns = [format_dict_value(column) for column in columns]
            columns_value = "columns: [" + ", ".join(formatted_columns) + "]"

        elif isinstance(columns, dict):
            columns_value = "columns: [" + format_dict_value(columns) + "]"

        else:
            raise TypeError(
                "Unsupported type for 'columns' parameter. Expected ItemByColumnValuesParam, dict, "
                "or list of dictionaries. For more information visit \n"
                "https://developer.monday.com/api-reference/reference/other-types#items-page-by-column-values-query"
            )

    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items_page_by_column_values (
            board_id: {format_param_value(board_id)},
            limit: {limit},
            cursor: {format_param_value(cursor)},
            {columns_value}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def next_items_page_query(cursor: str, limit: int = 500, with_complexity: bool = False, with_column_values: bool = True,
                          with_subitems: bool = False, with_updates: bool = False) -> str:
    """
    This query returns the next set of items that correspond with the provided cursor. For more information, visit
    https://developer.monday.com/api-reference/reference/items-page#cursor-based-pagination-using-next_items_page

    Args:
        cursor (str): An opaque cursor that represents the position in the list after the last returned item.
            Use this cursor for pagination to fetch the next set of items.
            If the cursor is null, there are no more items to fetch.

        limit (int): The number of items to return. 500 by default, the maximum is 500.

        with_complexity (bool): Set to True to return the query's complexity along with the results.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_subitems (bool): Set to True to return the items subitems along with the results. False by default.

        with_updates (bool): Set to True to return the items updates along with the results. False by default.

    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        next_items_page (
            cursor: {format_param_value(cursor)},
            limit: {limit}
        ) {{
            cursor
            items {{
                id
                name
                state
                {add_updates() if with_updates else ""}
                {add_column_values() if with_column_values else ""}
                {add_subitems() if with_subitems else ""}
                url
                group {{
                    id
                    title
                    color
                }}                
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_item_query(item_name: str, board_id: ID, group_id: Optional[str] = None,
                      column_values: Optional[dict] = None, create_labels_if_missing: bool = False,
                      with_complexity: bool = False) -> str:
    """
    This query creates a new item on a specified board and group with a given name and optional column values.
    For more information, visit https://developer.monday.com/api-reference/reference/items#create-an-item

    Args:
        item_name (str): The name of the new item.

        board_id (ID): The ID of the board to create the item on.

        group_id (str): (Optional) The ID of the group to create the item in.

        column_values (dict): (Optional) The column values for the new item in JSON format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_item (
            item_name: {format_param_value(item_name)},
            board_id: {format_param_value(board_id)},
            group_id: {format_param_value(group_id)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def duplicate_item_query(board_id: ID, item_id: ID, with_updates: Optional[bool] = None,
                         with_complexity: bool = False) -> str:
    """
    This query creates a copy of an item on the same board, with the option to include updates.
    For more information, visit https://developer.monday.com/api-reference/reference/items#duplicate-an-item

    Args:
        board_id (ID): The ID of the board containing the item to duplicate.

        with_updates (bool): (Optional) Whether to include the item's updates in the duplication.

        item_id (ID): The ID of the item to duplicate.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        duplicate_item (
            board_id: {format_param_value(board_id)},
            with_updates: {format_param_value(with_updates)},
            item_id: {format_param_value(item_id)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def archive_item_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query archives an item, making it no longer visible in the active item list.
    For more information, visit https://developer.monday.com/api-reference/reference/items#archive-an-item
    Args:

        item_id (ID): The ID of the item to archive.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        archive_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def delete_item_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query permanently removes an item from a board.
    For more information, visit https://developer.monday.com/api-reference/reference/items#delete-an-item

    Args:
        item_id (ID): The ID of the item to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_item (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def get_subitems_by_parent_item_query(parent_item_id: ID, with_column_values: bool = True,
                                      with_complexity: bool = False) -> str:
    """
    This query retrieves subitems of a specific item.
    For more information, visit https://developer.monday.com/api-reference/reference/subitems#queries

    Args:
        parent_item_id (ID): The ID of the parent item to retrieve subitems from.

        with_column_values (bool): Set to True to return the items column values along with the results.
            True by default.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (ids: {format_param_value(parent_item_id)}) {{
            subitems {{
                id
                name
                state
                {add_column_values() if with_column_values else ""}
                url
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_subitem_query(parent_item_id: ID, subitem_name: str, column_values: Optional[dict] = None,
                         create_labels_if_missing: bool = False, with_complexity: bool = False) -> str:
    """
    This query creates a new subitem under a specific parent item with a given name and optional column values.
    For more information, visit https://developer.monday.com/api-reference/reference/subitems#create-a-subitem

    Args:
        parent_item_id (ID): The ID of the parent item.

        subitem_name (str): The name of the new subitem.

        column_values (dict): (Optional) The column values for the new subitem in JSON format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_subitem (
            parent_item_id: {format_param_value(parent_item_id)},
            item_name: {format_param_value(subitem_name)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_multiple_item_column_values_query(item_id: ID, board_id: ID, column_values: dict,
                                             create_labels_if_missing: bool = False,
                                             with_complexity: bool = False) -> str:
    """
    This query updates the values of multiple columns for a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-multiple-column-values

    Args:
        item_id (ID): The ID of the item to update.

        board_id (ID): The ID of the board containing the item.

        column_values (dict): The updated column values as a dictionary in a {column_id: column_value, ...} format.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_multiple_column_values (
            item_id: {format_param_value(item_id)},
            board_id: {format_param_value(board_id)},
            column_values: {monday_json_stringify(column_values)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_item_column_json_value_query(item_id: ID, column_id: str, board_id: ID, value: dict,
                                        create_labels_if_missing: bool = False,
                                        with_complexity: bool = False) -> str:
    """
    This query updates the value of a specific column for an item using a JSON value. For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-column-value

    Args:
        item_id (ID): (Optional) The ID of the item to update.

        column_id (str): The unique identifier of the column to update.

        board_id (ID): The ID of the board containing the item.

        value (dict): The new value for the column as a dictionary.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_column_value (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            board_id: {format_param_value(board_id)},
            value: {monday_json_stringify(value)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def change_item_column_simple_value_query(item_id: ID, column_id: str, board_id: ID, value: str,
                                          create_labels_if_missing: bool = False,
                                          with_complexity: bool = False) -> str:
    """
    This query updates the value of a specific column for an item using a simple string value.
    For more information, visit
    https://developer.monday.com/api-reference/reference/columns#change-a-simple-column-value

    Args:
        item_id (ID): (Optional) The ID of the item to update.

        column_id (str): The unique identifier of the column to update.

        board_id (ID): The ID of the board containing the item.

        value (str): The new simple string value for the column. Use null to clear the column value.

        create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
            Requires permission to change board structure.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        change_simple_column_value (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            board_id: {format_param_value(board_id)},
            value: {format_param_value(value)},
            create_labels_if_missing: {format_param_value(create_labels_if_missing)}
        ) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def upload_file_to_column_query(item_id: ID, column_id: str, with_complexity: bool = False) -> str:
    """
    This query uploads a file and adds it to a specific column of an item. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-file-to-the-file-column

    Args:
        item_id (ID): The ID of the item to add the file to.

        column_id (str): The unique identifier of the column to add the file to.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation ($file: File!){{{add_complexity() if with_complexity else ""}
        add_file_to_column (
            item_id: {format_param_value(item_id)},
            column_id: {format_param_value(column_id)},
            file: $file
        ) {{
            id
            name
            url
        }}
    }}
    """
    return graphql_parse(query)


def get_item_updates_query(item_id: ID, ids: Union[ID, List[ID]] = None,
                           limit: int = 25, page: int = 1, with_complexity: bool = False) -> str:
    """
    This query retrieves updates associated with a specific item, allowing pagination and filtering by update IDs.

    Args:
        item_id (ID): The ID of the item to retrieve updates from.

        ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.

        limit (int): (Optional) The maximum number of updates to return. Defaults to 25.

        page (int): (Optional) The page number to return. Starts at 1.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        items (ids: {format_param_value(item_id)}) {{
            updates (ids: {format_param_value(ids if ids else None)}, limit: {limit}, page: {page}) {{
                id
                text_body
                body
                creator_id
                assets {{
                    id 
                    name
                    file_extension
                    url
                    public_url 
                }}
                replies {{
                    id
                    text_body
                }}
                likes {{
                    id
                    reaction_type
                    creator_id
                    updated_at
                }}
            }}
        }}
    }}
    """
    return graphql_parse(query)


def clear_item_updates_query(item_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes all updates associated with a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/items#clear-an-items-updates

    Args:
        item_id (ID): The ID of the item to clear updates from.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        clear_item_updates (item_id: {format_param_value(item_id)}) {{
            id
            name
        }}
    }}
    """
    return graphql_parse(query)


def move_item_to_group_query(item_id: ID, group_id: str, with_complexity: bool = False) -> str:
    """
    This query moves an item to a different group within the same board. For more information, visit
    https://developer.monday.com/api-reference/reference/items#move-item-to-group

    Args:
        item_id (ID): The ID of the item to move.

        group_id (str): The ID of the target group within the board.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        move_item_to_group (
            item_id: {format_param_value(item_id)},
            group_id: {format_param_value(group_id)}
        ) {{
            id
            name
            group {{
                id
                title
                color
            }}
        }}
    }}
    """
    return graphql_parse(query)


# ### UPDATE RESOURCE QUERIES ### #
def get_updates_query(ids: Union[ID, List[ID]] = None, limit: int = 25, page: int = 1,
                      with_complexity: bool = False) -> str:
    """
    This query retrieves updates, allowing pagination and filtering by update IDs. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#queries

    Args:
        ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.
        limit (int): (Optional) The maximum number of updates to return. Defaults to 25.
        page (int): (Optional) The page number to return. Starts at 1.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        updates (ids: {format_param_value(ids if ids else None)}, limit: {limit}, page: {page}) {{
            id
            text_body
            body
            creator_id
            assets {{
                id 
                name
                file_extension
                url
                public_url 
            }}
            replies {{
                id
                text_body
            }}
            likes {{
                id
                reaction_type
                creator_id
                updated_at
            }}
        }}
    }}
    """
    return graphql_parse(query)


def create_update_query(body: str, item_id: ID, parent_id: Optional[ID] = None, with_complexity: bool = False) -> str:
    """
    This query creates a new update on a specific item or as a reply to another update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#create-an-update

    Args:
        body (str): The text content of the update as a string or in HTML format.

        item_id (ID): The ID of the item to create the update on.

        parent_id (ID): (Optional) The ID of the parent update to reply to.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_update (
            body: {format_param_value(body)},
            item_id: {format_param_value(item_id)},
            parent_id: {format_param_value(parent_id)}
        ) {{
            id
            body
        }}
    }}
    """
    return graphql_parse(query)


def edit_update_query(update_id: ID, body: str, with_complexity: bool = False) -> str:
    """
    This query allows you to edit an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#edit-an-update

    Args:
        update_id (ID): The ID of the update to edit.
        body (str): The new text content of the update as a string or in HTML format.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        edit_update (
            id: {format_param_value(update_id)},
            body: {format_param_value(body)}
        ) {{
            id
            body
        }}
    }}
    """
    return graphql_parse(query)


def pin_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query pins an update to the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#pin-an-update
    Args:
        update_id (ID): The ID of the update to pin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        pin_to_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
        }}
    }}
    """
    return graphql_parse(query)


def unpin_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query unpins an update from the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unpin-an-update
    Args:
        update_id (ID): The ID of the update to unpin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unpin_from_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
        }}
    }}
    """
    return graphql_parse(query)


def like_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query adds a like to a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#like-an-update

    Args:
        update_id (ID): The ID of the update to like.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        like_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(query)


def unlike_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes a like from a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unlike-an-update

    Args:
        update_id (ID): The ID of the update to unlike.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unlike_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(query)


def delete_update_query(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query removes an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#delete-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_update (id: {format_param_value(update_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(query)


def add_file_to_update(update_id: ID, with_complexity: bool = False) -> str:
    """
    This query adds a file to an update. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-a-file-to-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """

    query = f"""
    mutation ($file: File!){{{add_complexity() if with_complexity else ""}
        add_file_to_update (update_id: {format_param_value(update_id)}, file: $file) {{
            id
        }}
    }}
    """
    return graphql_parse(query)
