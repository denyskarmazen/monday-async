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


from monday_async.graphql.mutations import (
    add_file_to_update_mutation,
    create_update_mutation,
    delete_update_mutation,
    edit_update_mutation,
    like_update_mutation,
    pin_update_mutation,
    unlike_update_mutation,
    unpin_update_mutation,
)
from monday_async.graphql.queries import get_updates_query
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ID, MentionInput


class UpdateResource(AsyncBaseResource):
    """
    monday.com updates contain additional notes and information added to items outside of their columns.
    Updates allow users to organize communication across their organization and respond asynchronously.
    For many users, the updates section is their primary form of communication within the platform.
    """

    async def get_updates(
        self,
        ids: ID | list[ID] = None,
        limit: int = 25,
        page: int = 1,
        with_viewers: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve updates, allowing pagination and filtering by update IDs.

        For more information, visit https://developer.monday.com/api-reference/reference/updates#queries

        Args:
            ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.
            limit (int): (Optional) The maximum number of updates to return. Defaults to 25.
            page (int): (Optional) The page number to return. Starts at 1.
            with_viewers (bool): Set to True to return the viewers of the update.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_updates_query(
            ids=ids, limit=limit, page=page, with_viewers=with_viewers, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def create_update(
        self,
        body: str,
        item_id: ID,
        parent_id: ID | None = None,
        mentions_list: MentionInput | None = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a new update on a specific item or as a reply to another update.

        For more information, visit https://developer.monday.com/api-reference/reference/updates#create-an-update

        Args:
            body (str): The text content of the update as a string or in HTML format.
            item_id (ID): The ID of the item to create the update on.
            parent_id (ID): (Optional) The ID of the parent update to reply to.
            mentions_list (MentionInput): (Optional) A list of users or teams to mention in the update.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = create_update_mutation(
            body=body,
            item_id=item_id,
            parent_id=parent_id,
            mentions_list=mentions_list,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def edit_update(self, update_id: ID, body: str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to edit the content of an update.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#edit-an-update

        Args:
            update_id (ID): The ID of the update to edit.
            body (str): The updated text content of the update as a string or in HTML format.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        mutation = edit_update_mutation(update_id=update_id, body=body, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def pin_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to pin an update to the top of the updates section of a specific item.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#pin-an-update

        Args:
            update_id (ID): The ID of the update to pin.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        mutation = pin_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def unpin_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to unpin an update from the top of the updates section of a specific item.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#unpin-an-update

        Args:
            update_id (ID): The ID of the update to unpin.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        mutation = unpin_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def like_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to add a like to a specific update.

        For more information, visit https://developer.monday.com/api-reference/reference/updates#like-an-update

        Args:
            update_id (ID): The ID of the update to like.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = like_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def unlike_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to remove a like from a specific update.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#unlike-an-update

        Args:
            update_id (ID): The ID of the update to unlike.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        mutation = unlike_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def delete_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to remove an update. For more information, visit
        https://developer.monday.com/api-reference/reference/updates#delete-an-update

        Args:
            update_id (ID): The unique identifier of the update to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def add_file_to_update(self, update_id: ID, file: str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to add a file to an update. For more information, visit
        https://developer.monday.com/api-reference/reference/assets-1#add-a-file-to-an-update

        Args:
            update_id (ID): The unique identifier of the update to delete.
            file (str): The filepath to the file.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = add_file_to_update_mutation(update_id=update_id, with_complexity=with_complexity)
        return await self.file_upload_client.execute(mutation, variables={"file": file})
