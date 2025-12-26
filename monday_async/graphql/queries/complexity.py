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
from monday_async.graphql.addons import add_complexity


def get_complexity_query() -> str:
    """
    Construct a query to get the current complexity points. For more information visit
    https://developer.monday.com/api-reference/reference/complexity
    """
    query = f"""query {{{add_complexity()}}}"""
    return graphql_parse(query)


__all__ = ["get_complexity_query"]
