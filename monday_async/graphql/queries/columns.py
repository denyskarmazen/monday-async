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
from monday_async.types import ID, ColumnType


def get_columns_by_board_query(
    board_id: ID,
    ids: ID | list[ID] = None,
    types: ColumnType | list[ColumnType] = None,
    with_complexity: bool = False,
) -> str:
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


__all__ = [
    "get_columns_by_board_query",
]
