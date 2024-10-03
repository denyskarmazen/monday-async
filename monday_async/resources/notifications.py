from typing import Union

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import TargetType
from monday_async.utils.queries import create_notification_query


class NotificationResource(AsyncBaseResource):
    async def create_notification(self, user_id: Union[int, str], target_id: Union[int, str], text: str,
                                  target_type: TargetType, with_complexity: bool = False) -> dict:
        """
        Create a notification. For more information, visit
        https://developer.monday.com/api-reference/reference/notification

        Args:
            user_id (Union[int, str]): the user's unique identifier.
            target_id (Union[int, str]): the target's unique identifier. The value depends on the target_type:
                - Project: the relevant item or board ID
                - Post : the relevant update or reply ID
            text (str): the notification's text.
            target_type (TargetType): the target's type: project or post.
                - Project: sends a notification referring to a specific item or board
                - Post : sends a notification referring to a specific item's update or reply
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = create_notification_query(user_id=user_id, target_id=target_id, text=text, target_type=target_type,
                                          with_complexity=with_complexity)
        return await self.client.execute(query)
