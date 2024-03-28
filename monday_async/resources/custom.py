from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.utils.utils import graphql_parse


class CustomResource(AsyncBaseResource):
    async def execute_custom_query(self, custom_query):
        parsed_query = graphql_parse(custom_query)
        return await self.client.execute(parsed_query)

    async def execute_custom_file_query(self, custom_query):
        parsed_query = graphql_parse(custom_query)
        return await self.file_upload_client.execute(parsed_query)
