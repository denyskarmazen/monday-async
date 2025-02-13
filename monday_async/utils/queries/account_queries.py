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

from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import graphql_parse


def get_account_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get the account details. For more information, visit
    https://developer.monday.com/api-reference/reference/account

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed query.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        account {{
            id
            name
            slug
            tier
            country_code
            plan {{
                max_users
                tier
                period
                version
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_account_query'
]
