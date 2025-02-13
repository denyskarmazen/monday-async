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
