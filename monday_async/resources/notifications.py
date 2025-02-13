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

from typing import Union

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import NotificationTargetType
from monday_async.utils.queries import create_notification_query


class NotificationResource(AsyncBaseResource):
    async def create_notification(self, user_id: Union[int, str], target_id: Union[int, str], text: str,
                                  target_type: NotificationTargetType, with_complexity: bool = False) -> dict:
        """
        Create a notification. For more information, visit
        https://developer.monday.com/api-reference/reference/notification

        Args:
            user_id (Union[int, str]): the user's unique identifier.
            target_id (Union[int, str]): the target's unique identifier. The value depends on the target_type:
                - Project: the relevant item or board ID
                - Post : the relevant update or reply ID
            text (str): the notification's text.
            target_type (NotificationTargetType): the target's type: project or post.
                - Project: sends a notification referring to a specific item or board
                - Post : sends a notification referring to a specific item's update or reply
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = create_notification_query(user_id=user_id, target_id=target_id, text=text, target_type=target_type,
                                          with_complexity=with_complexity)
        return await self.client.execute(query)
