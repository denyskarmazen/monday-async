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
