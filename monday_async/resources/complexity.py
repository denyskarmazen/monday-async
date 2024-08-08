from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.utils.queries import get_complexity_query


class ComplexityResource(AsyncBaseResource):
    async def get_complexity(self) -> dict:
        """
        Get the current complexity points. For more information visit
        https://developer.monday.com/api-reference/reference/complexity
        """

        query = get_complexity_query()
        return await self.client.execute(query)
