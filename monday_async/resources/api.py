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
from monday_async.utils.queries import get_current_api_version_query, get_all_api_versions_query


class APIResource(AsyncBaseResource):
    async def get_current_api_version(self, with_complexity: bool = False) -> dict:
        """
        Get the api version that is used to make the request. For more information, visit
        https://developer.monday.com/api-reference/reference/version

        Args:
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = get_current_api_version_query(with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_all_api_versions(self, with_complexity: bool = False) -> dict:
        """
        Get all the monday.com api versions available. For more information, visit
        https://developer.monday.com/api-reference/reference/versions

        Args:
            with_complexity (bool): returns the complexity of the query with the query if set to True.
        """
        query = get_all_api_versions_query(with_complexity=with_complexity)
        return await self.client.execute(query)
