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


def create_or_get_tag_mutation(tag_name: str, board_id: ID | None = None, with_complexity: bool = False) -> str:
    """
    This mutation creates a new tag with the specified name or retrieves the existing tag if it already exists.
    For more information, visit https://developer.monday.com/api-reference/reference/tags-1#create-or-get-a-tag

    Args:
        tag_name (str): The name of the tag to create or retrieve.

        board_id (ID): (Optional) The ID of the private board to create the tag in. Not needed for public boards.

        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
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
    return graphql_parse(mutation)


__all__ = ["create_or_get_tag_mutation"]
