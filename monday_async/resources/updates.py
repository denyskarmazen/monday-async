from typing import List, Union, Optional

from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.utils.queries import (
    get_updates_query, create_update_query, like_update_query, delete_update_query, add_file_to_update,
    pin_update_query, unpin_update_query, unlike_update_query, edit_update_query
)

ID = Union[int, str]


class UpdateResource(AsyncBaseResource):
    """
    monday.com updates contain additional notes and information added to items outside of their columns.
    Updates allow users to organize communication across their organization and respond asynchronously.
    For many users, the updates section is their primary form of communication within the platform.
    """

    async def get_updates(self, ids: Union[ID, List[ID]] = None, limit: int = 25, page: int = 1,
                          with_viewers: bool = False, with_complexity: bool = False) -> dict:
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
        query = get_updates_query(ids=ids, limit=limit, page=page, with_viewers=with_viewers,
                                  with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_update(self, body: str, item_id: ID, parent_id: Optional[ID] = None,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to create a new update on a specific item or as a reply to another update.

        For more information, visit https://developer.monday.com/api-reference/reference/updates#create-an-update

        Args:
            body (str): The text content of the update as a string or in HTML format.
            item_id (ID): The ID of the item to create the update on.
            parent_id (ID): (Optional) The ID of the parent update to reply to.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_update_query(body=body, item_id=item_id, parent_id=parent_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def edit_update(self, update_id: ID, body: str, with_complexity: bool = False) -> dict:
        """
        Edit the content of an update.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#edit-an-update

        Args:
            update_id (ID): The ID of the update to edit.
            body (str): The updated text content of the update as a string or in HTML format.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        query = edit_update_query(update_id=update_id, body=body, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def pin_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to pin  an update to the top of the updates section of a specific item.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#pin-an-update

        Args:
            update_id (ID): The ID of the update to pin.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        query = pin_update_query(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def unpin_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to unpin an update from the top of the updates section of a specific item.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#unpin-an-update

        Args:
            update_id (ID): The ID of the update to unpin.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        query = unpin_update_query(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def like_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to add a like to a specific update.

        For more information, visit https://developer.monday.com/api-reference/reference/updates#like-an-update

        Args:
            update_id (ID): The ID of the update to like.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = like_update_query(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def unlike_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to remove a like from a specific update.
        For more information, visit https://developer.monday.com/api-reference/reference/updates#unlike-an-update

        Args:
            update_id (ID): The ID of the update to unlike.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        query = unlike_update_query(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_update(self, update_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a query to remove an update. For more information, visit
        https://developer.monday.com/api-reference/reference/updates#delete-an-update

        Args:
            update_id (ID): The unique identifier of the update to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_update_query(update_id=update_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def add_file_to_update(self, update_id: ID, file: str, with_complexity: bool = False) -> dict:
        """
        Execute a query to add a file to an update. For more information, visit
        https://developer.monday.com/api-reference/reference/assets-1#add-a-file-to-an-update

        Args:
            update_id (ID): The unique identifier of the update to delete.
            file (str): The filepath to the file.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = add_file_to_update(update_id=update_id, with_complexity=with_complexity)
        return await self.file_upload_client.execute(query, variables={"file": file})
