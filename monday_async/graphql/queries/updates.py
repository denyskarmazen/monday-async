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


from monday_async.core.helpers import graphql_parse
from monday_async.graphql.addons import add_complexity, add_updates
from monday_async.types import ID


def get_updates_query(
    ids: ID | list[ID] | None = None,
    limit: int = 25,
    page: int = 1,
    with_viewers: bool = False,
    with_complexity: bool = False,
) -> str:
    """
    This query retrieves updates, allowing pagination and filtering by update IDs. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#queries

    Args:
        ids (Union[ID, List[ID]]): A list of update IDs to retrieve specific updates.
        limit (int): the maximum number of updates to return. Defaults to 25. Maximum is 100 per page.
        page (int): The page number to return. Starts at 1.
        with_viewers (bool): Set to True to return the viewers of the update.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    if ids and isinstance(ids, list):
        limit = len(ids)
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        {add_updates(ids=ids, limit=limit, page=page, with_viewers=with_viewers, with_pins=True, with_likes=True)}
    }}
    """
    return graphql_parse(query)


__all__ = [
    "get_updates_query",
]
