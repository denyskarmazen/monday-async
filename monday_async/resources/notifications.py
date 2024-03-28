from monday_async.resources.base_resource import AsyncBaseResource
from typing import Union
from monday_async.utils.queries import create_notification_query
from monday_async.utils.types import TargetType


class NotificationResource(AsyncBaseResource):
    async def create_notification(self, user_id: Union[int, str], target_id: Union[int, str], text: str,
                                  target_type: TargetType, with_complexity: bool = False):
        query = create_notification_query(user_id=user_id, target_id=target_id, text=text, target_type=target_type,
                                          with_complexity=with_complexity)
        return await self.client.execute(query)
