from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (
    get_columns_by_board_query, create_column_query,
    change_column_title_query, change_column_description_query,
    delete_column_query
)
from monday_async.types import ColumnType


ID = Union[int, str]


class ColumnResource(AsyncBaseResource):
    async def get_columns_by_board(self, board_id: ID, ids: Union[ID, List[ID]] = None,
                                   types: Union[ColumnType, List[ColumnType]] = None,
                                   with_complexity: bool = False) -> dict:
        """
        Execute a query to retrieve columns associated with a specific board, allowing filtering by column IDs and types.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#queries

        Parameters:
            board_id (ID): The ID of the board to retrieve columns from.
            ids (Union[ID, List[ID]]): (Optional) A list of column IDs to retrieve specific columns.
            types (List[ColumnType]): (Optional) A list of column types to filter by.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_columns_by_board_query(board_id=board_id, ids=ids, types=types, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_column(self, board_id: ID, title: str, column_type: ColumnType,
                            description: Optional[str] = None, defaults: Optional[dict] = None,
                            column_id: Optional[str] = None, after_column_id: Optional[ID] = None,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to create a new column on a specific board with a specified title, type,
        and optional description, defaults, user-specified ID, and positioning.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#create-a-column

        Parameters:
            board_id (ID): The ID of the board to create the column on.
            title (str): The title of the new column.
            column_type (ColumnType): The type of column to create, chosen from the ColumnType enum.
            description (str): (Optional) A description for the new column.
            defaults (dict): (Optional) The default value for the new column as a dictionary.
            column_id (str): (Optional) A user-specified unique identifier for the column. Has to meet requirements:
                - [1-20] characters in length (inclusive)
                - Only lowercase letters (a-z) and underscores (_)
                - Must be unique (no other column on the board can have the same ID)
                - Can't reuse column IDs, even if the column has been deleted from the board
                - Can't be null, blank, or an empty string
            after_column_id (ID): (Optional) The ID of the column after which to insert the new column.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_column_query(board_id=board_id, title=title, column_type=column_type,
                                    description=description, defaults=defaults, column_id=column_id,
                                    after_column_id=after_column_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def change_column_title(self, board_id: ID, column_id: str, title: str,
                                  with_complexity: bool = False) -> dict:
        """
        Execute a query to update the title of an existing column on a specific board.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#change-a-column-title

        Parameters:
            board_id (ID): The ID of the board containing the column.
            column_id (str): The unique identifier of the column to update.
            title (str): The new title for the column.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = change_column_title_query(board_id=board_id, column_id=column_id, title=title,
                                          with_complexity=with_complexity)
        return await self.client.execute(query)

    async def change_column_description(self, board_id: ID, column_id: str, description: str,
                                        with_complexity: bool = False) -> dict:
        """
        Execute a query to update the description of an existing column on a specific board.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#change-column-metadata

        Parameters:
            board_id (ID): The ID of the board containing the column.
            column_id (str): The unique identifier of the column to update.
            description (str): The new description for the column.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = change_column_description_query(board_id=board_id, column_id=column_id,
                                                description=description, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_column(self, board_id: ID, column_id: str,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to remove a column from a specific board.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#delete-a-column

        Parameters:
            board_id (ID): The ID of the board containing the column.
            column_id (str): The unique identifier of the column to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_column_query(board_id=board_id, column_id=column_id, with_complexity=with_complexity)
        return await self.client.execute(query)
