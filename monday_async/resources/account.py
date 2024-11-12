from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.utils.queries import get_account_query


class AccountResource(AsyncBaseResource):
    async def get_account(self, with_complexity: bool = False) -> dict:
        """
        Get the account details of the current user. For more information, visit
        https://developer.monday.com/api-reference/reference/account

        Args:
            with_complexity (bool): Returns the complexity of the query with the query if set to True.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        query = get_account_query(with_complexity=with_complexity)
        return await self.client.execute(query)
