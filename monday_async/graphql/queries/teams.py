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


def get_teams_query(team_ids: ID | list[ID] = None, with_complexity: bool = False) -> str:
    """
    Construct a query to get all teams or get teams by ids if provided. For more information, visit
    https://developer.monday.com/api-reference/reference/teams#queries

    Args:
        team_ids (Union[int, str, List[Union[int, str]]]):
            A single team ID, a list of team IDs, or None to get all teams.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        teams (ids: {format_param_value(team_ids if team_ids else None)}) {{
            id
            name
            users {{
                id
                email
                name
                is_guest
            }}
            owners {{
                id
                name
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    "get_teams_query",
]
