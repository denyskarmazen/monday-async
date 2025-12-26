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
from monday_async.types import ID


def get_tags_query(ids: ID | list[ID] = None, with_complexity: bool = False) -> str:
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


__all__ = ["get_tags_by_board_query", "get_tags_query"]
