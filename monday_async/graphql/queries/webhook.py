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


def get_webhooks_by_board_id_query(board_id: ID, app_webhooks_only: bool = False, with_complexity: bool = False) -> str:
    """
    Construct a query to get all webhooks for a board. For more information, visit
    https://developer.monday.com/api-reference/reference/webhooks#queries

    Args:
        board_id (Union[int, str]): a unique identifier of a board, can be an integer or
            a string containing integers.
        app_webhooks_only (bool): if set to Trues returns only the webhooks created by the app initiating the request.
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        webhooks(
            app_webhooks_only: {format_param_value(app_webhooks_only)},
            board_id: {format_param_value(board_id)}
        ) {{
            id
            event
            board_id
            config
        }}
    }}
    """
    return graphql_parse(query)


__all__ = ["get_webhooks_by_board_id_query"]
