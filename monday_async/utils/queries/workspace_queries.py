from enum import Enum
from typing import List, Union, Optional

from monday_async.types import WorkspaceKind, State, SubscriberKind, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


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
    update_params = [
        value for value in [
            f"name: {format_param_value(name)}" if name else None,
            f"kind: {kind.value if isinstance(kind, Enum) else kind}" if kind else None,
            f"description: {format_param_value(description)}" if description else None
        ] if value is not None
    ]
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_workspace (
            id: {format_param_value(workspace_id)},
            attributes: {{{', '.join(update_params)}}}
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


__all__ = [
    "get_workspaces_query",
    "create_workspace_query",
    "update_workspace_query",
    "delete_workspace_query",
    "add_users_to_workspace_query",
    "delete_users_from_workspace_query",
    "add_teams_to_workspace_query",
    "delete_teams_from_workspace_query"
]
