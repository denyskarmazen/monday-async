from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (
    get_tags_query, get_tags_by_board_query, create_or_get_tag_query
)

ID = Union[int, str]


class TagResource(AsyncBaseResource):
    async def get_tags(self, ids: Union[ID, List[ID]] = None,
                       with_complexity: bool = False) -> str:
        """
        Execute a query to retrieve tags, allowing you to specify individual tags or retrieve all tags.

        For more information, visit https://developer.monday.com/api-reference/reference/tags-1#queries

        Parameters:
            ids (Union[ID, List[ID]]): (Optional) A list of tag IDs to retrieve specific tags.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_tags_query(ids=ids, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_tags_by_board(self, board_id: ID, with_complexity: bool = False) -> str:
        """
        Execute a query to retrieve tags associated with a specific board.

        For more information, visit https://developer.monday.com/api-reference/reference/tags-1#queries

        Parameters:
            board_id (ID): The ID of the board to retrieve tags from.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_tags_by_board_query(board_id=board_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_or_get_tag(self, tag_name: str, board_id: Optional[ID] = None,
                                with_complexity: bool = False) -> str:
        """
        Execute a query to create a new tag with the specified name or retrieve the existing tag if it already exists.

        For more information, visit https://developer.monday.com/api-reference/reference/tags-1#create-or-get-a-tag

        Parameters:
            tag_name (str): The name of the tag to create or retrieve.
            board_id (ID): (Optional) The ID of the private board to create the tag in. Not needed for public boards.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_or_get_tag_query(tag_name=tag_name, board_id=board_id, with_complexity=with_complexity)
        return await self.client.execute(query)
