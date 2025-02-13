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

from monday_async.types import NotificationTargetType, ID
from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import format_param_value, graphql_parse


def create_notification_query(user_id: ID, target_id: ID, text: str, target_type: NotificationTargetType,
                              with_complexity: bool = False) -> str:
    """
    Construct a query to create a notification. For more information, visit
    https://developer.monday.com/api-reference/reference/notification

    Args:
        user_id (ID): the user's unique identifier.
        target_id (ID): the target's unique identifier. The value depends on the target_type:
            - Project: the relevant item or board ID
            - Post : the relevant update or reply ID

        text (str): the notification's text.

        target_type (NotificationTargetType): the target's type: project or post.
            - Project: sends a notification referring to a specific item or board
            - Post : sends a notification referring to a specific item's update or reply

        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    target_type_value = target_type.value if isinstance(target_type, NotificationTargetType) else target_type
    query = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_notification (
            user_id: {format_param_value(user_id)},
             target_id: {format_param_value(target_id)},
             text: {format_param_value(text)},
             target_type: {target_type_value}
        ) {{
            text
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'create_notification_query'
]
