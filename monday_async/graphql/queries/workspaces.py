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


from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, State, WorkspaceKind


def get_workspaces_query(
    workspace_ids: ID | list[ID] = None,
    limit: int = 25,
    page: int = 1,
    kind: WorkspaceKind | None = None,
    with_complexity: bool = False,
    state: State = State.ACTIVE,
) -> str:
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


__all__ = [
    "get_workspaces_query",
]
