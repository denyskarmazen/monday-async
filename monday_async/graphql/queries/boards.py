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
from monday_async.graphql.addons import add_columns, add_complexity, add_groups
from monday_async.types import ID, BoardKind, BoardsOrderBy, State


def get_boards_query(
    ids: ID | list[ID] = None,
    board_kind: BoardKind | None = None,
    state: State = State.ACTIVE,
    workspace_ids: ID | list[ID] = None,
    order_by: BoardsOrderBy | None = None,
    limit: int = 25,
    page: int = 1,
    with_columns: bool = True,
    with_groups: bool = True,
    with_complexity: bool = False,
) -> str:
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
        with_columns (bool): (Optional) Set to True to include columns in the query results.
        with_groups (bool): (Optional) Set to True to include groups in the query results.
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
            {add_groups() if with_groups else ""}
            {add_columns() if with_columns else ""}
            item_terminology
            subscribers {{
                name
                id
            }}
        }}
    }}
    """
    return graphql_parse(query)


def get_board_views_query(
    board_id: ID, ids: ID | list[ID] = None, view_type: str | None = None, with_complexity: bool = False
) -> str:
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


__all__ = ["get_board_views_query", "get_boards_query"]
