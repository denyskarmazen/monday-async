from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.utils.utils import graphql_parse


class CustomResource(AsyncBaseResource):
    async def execute_custom_query(self, custom_query: str) -> dict:
        """
        Execute a custom GraphGL query

        Args:
            custom_query(str): The custom query to execute.
        """
        parsed_query = graphql_parse(custom_query)
        return await self.client.execute(parsed_query)

    async def execute_custom_file_upload_query(self, custom_query: str) -> dict:
        """
        Execute a custom GraphGL file upload query. For more information, visit
         https://developer.monday.com/api-reference/reference/assets-1#files-endpoint

        Args:
            custom_query(str): The custom query to execute.
        """
        parsed_query = graphql_parse(custom_query)
        return await self.file_upload_client.execute(parsed_query)
