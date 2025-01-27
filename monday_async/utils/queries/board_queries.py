from typing import List, Union, Optional

from monday_async.types import (State, SubscriberKind, BoardKind, BoardAttributes, DuplicateBoardType,
                                BoardsOrderBy, ID)
from monday_async.utils.queries.query_addons import add_complexity, add_columns, add_groups
from monday_async.utils.utils import format_param_value, graphql_parse


def get_boards_query(ids: Union[ID, List[ID]] = None, board_kind: Optional[BoardKind] = None,
                     state: State = State.ACTIVE, workspace_ids: Union[ID, List[ID]] = None,
                     order_by: Optional[BoardsOrderBy] = None, limit: int = 25, page: int = 1,
                     with_columns: bool = True, with_groups: bool = True, with_complexity: bool = False) -> str:
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


def create_board_query(board_name: str, board_kind: BoardKind, description: Optional[str] = None,
                       folder_id: Optional[ID] = None, workspace_id: Optional[ID] = None,
                       template_id: Optional[ID] = None, board_owner_ids: List[ID] = None,
                       board_owner_team_ids: List[ID] = None, board_subscriber_ids: List[ID] = None,
                       board_subscriber_teams_ids: List[ID] = None, empty: bool = False,
                       with_columns: bool = False, with_groups: bool = False, with_complexity: bool = False) -> str:
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
        with_columns (bool): (Optional) Set to True to include columns in the query results. Defaults to False.
        with_groups (bool): (Optional) Set to True to include groups in the query results. Defaults to False.
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
            {add_groups() if with_groups else ""}
            {add_columns() if with_columns else ""}
        }}
    }}
    """
    return graphql_parse(query)


def duplicate_board_query(board_id: ID, duplicate_type: DuplicateBoardType,
                          board_name: Optional[str] = None, workspace_id: Optional[ID] = None,
                          folder_id: Optional[ID] = None, keep_subscribers: bool = False,
                          with_columns: bool = False, with_groups: bool = False, with_complexity: bool = False) -> str:
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
        with_columns (bool): (Optional) Set to True to include columns in the query results. Defaults to False.
        with_groups (bool): (Optional) Set to True to include groups in the query results. Defaults to False.
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
                {add_groups() if with_groups else ""}
                {add_columns() if with_columns else ""}
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
            name
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
            name
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


__all__ = [
    'get_boards_query',
    'create_board_query',
    'duplicate_board_query',
    'update_board_query',
    'archive_board_query',
    'delete_board_query',
    'add_users_to_board_query',
    'remove_users_from_board_query',
    'add_teams_to_board_query',
    'delete_teams_from_board_query',
    'get_board_views_query'
]
