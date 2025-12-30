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

from enum import Enum

from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, SubscriberKind, WorkspaceKind


def create_workspace_mutation(
    name: str,
    kind: WorkspaceKind,
    description: str | None = None,
    account_product_id: ID | None = None,
    with_complexity: bool = False,
):
    """
    Construct a mutation to create a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#create-a-workspace

    Args:
        name (str): The new workspace name.

        kind (WorkspaceKind): The new workspace kind: open or closed.

        description (Optional[str]): The new workspace description.

        account_product_id (Optional[ID]): The unique identifier of the account's product
            in which to create the new workspace.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    workspace_kind_value = kind.value if isinstance(kind, WorkspaceKind) else kind
    account_product_id_param = (
        f"account_product_id: {format_param_value(account_product_id)}," if account_product_id else ""
    )
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_workspace (
            name:{format_param_value(name)},
            kind: {workspace_kind_value},
            description: {format_param_value(description)},
            {account_product_id_param}
        ) {{
            id
            name
            description
            kind
        }}
    }}
    """
    return graphql_parse(mutation)


def update_workspace_mutation(
    workspace_id: ID,
    name: str | None = None,
    kind: WorkspaceKind | None = None,
    description: str | None = None,
    with_complexity: bool = False,
):
    """
    Construct a mutation to update a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#update-a-workspace

    Args:
        workspace_id (Union[int, str]): The unique identifier of the workspace to update.

        name (str): The updated workspace name.

        kind (WorkspaceKind): The kind of workspace to update: open or closed.

        description (Optional[str]): The updated workspace description.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    update_params = [
        value
        for value in [
            f"name: {format_param_value(name)}" if name else None,
            f"kind: {kind.value if isinstance(kind, Enum) else kind}" if kind else None,
            f"description: {format_param_value(description)}" if description else None,
        ]
        if value is not None
    ]
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_workspace (
            id: {format_param_value(workspace_id)},
            attributes: {{{", ".join(update_params)}}}
        ) {{
            id
            name
            description
            kind
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_workspace_mutation(workspace_id: int | str, with_complexity: bool = False):
    """
    Construct a mutation to delete a workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-a-workspace

    Args:
        workspace_id (Union[int, str]): The unique identifier of the workspace to delete.

        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_workspace (workspace_id: {workspace_id}) {{
            id
        }}
    }}
    """
    return graphql_parse(mutation)


def add_users_to_workspace_mutation(
    workspace_id: ID, user_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
) -> str:
    """
    This mutation adds users as subscribers or owners to a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#add-users-to-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to add to the workspace.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind
    mutation = f"""
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
    return graphql_parse(mutation)


def delete_users_from_workspace_mutation(
    workspace_id: ID, user_ids: ID | list[ID], with_complexity: bool = False
) -> str:
    """
    This mutation removes users from a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-users-from-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        user_ids (Union[ID, List[ID]]): A single user ID or a list of user IDs to remove from the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


def add_teams_to_workspace_mutation(
    workspace_id: ID, team_ids: ID | list[ID], kind: SubscriberKind, with_complexity: bool = False
) -> str:
    """
    This mutation adds teams as subscribers or owners to a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#add-teams-to-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to add to the workspace.

        kind (SubscriberKind): The type of subscription to grant: subscriber or owner.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    kind_value = kind.value if isinstance(kind, SubscriberKind) else kind

    mutation = f"""
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
    return graphql_parse(mutation)


def delete_teams_from_workspace_mutation(
    workspace_id: ID, team_ids: ID | list[ID], with_complexity: bool = False
) -> str:
    """
    This mutation removes teams from a specific workspace. For more information, visit
    https://developer.monday.com/api-reference/reference/workspaces#delete-teams-from-a-workspace

    Args:
        workspace_id (ID): The unique identifier of the target workspace.

        team_ids (Union[ID, List[ID]]): A single team ID or a list of team IDs to remove from the workspace.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


__all__ = [
    "add_teams_to_workspace_mutation",
    "add_users_to_workspace_mutation",
    "create_workspace_mutation",
    "delete_teams_from_workspace_mutation",
    "delete_users_from_workspace_mutation",
    "delete_workspace_mutation",
    "update_workspace_mutation",
]
