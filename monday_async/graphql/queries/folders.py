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


def get_folders_query(
    ids: ID | list[ID] = None,
    workspace_ids: ID | list[ID] = None,
    limit: int = 25,
    page: int = 1,
    with_complexity: bool = False,
) -> str:
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


__all__ = [
    "get_folders_query",
]
