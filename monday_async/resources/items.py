from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional
from monday_async.utils.queries import (
    get_items_by_id_query, get_items_by_board_query, get_items_by_group_query,
    get_items_by_column_value_query, get_items_by_multiple_column_values_query,
    next_items_page_query, create_item_query, duplicate_item_query,
    archive_item_query, delete_item_query, get_subitems_by_parent_item_query,
    create_subitem_query, change_multiple_item_column_values_query,
    change_item_column_json_value_query, change_item_column_simple_value_query,
    upload_file_to_column_query, get_item_updates_query, clear_item_updates_query,
    move_item_to_group_query
)
from monday_async.utils.types import QueryParams, ItemByColumnValuesParam

ID = Union[int, str]


class ItemResource(AsyncBaseResource):
    async def get_items_by_id(self, ids: Union[ID, List[ID]], newest_first: Optional[bool] = None,
                              exclude_nonactive: Optional[bool] = None, limit: int = 25, page: int = 1,
                              with_complexity: bool = False, with_column_values: bool = True,
                              with_subitems: bool = False, with_updates: bool = False) -> str:
        """
        Execute a query to retrieve items, allowing filtering by IDs, sorting, and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items#queries

        Parameters:
            ids (Union[ID, List[ID]]): A list of item IDs to retrieve specific items.
            newest_first (bool): (Optional) Set to True to order results with the most recently created items first.
            exclude_nonactive (bool): (Optional) Set to True to exclude inactive, deleted,
                or items belonging to deleted items.
            limit (int): (Optional) The maximum number of items to return. Defaults to 25.
            page (int): (Optional) The page number to return. Starts at 1.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = get_items_by_id_query(ids=ids, newest_first=newest_first, exclude_nonactive=exclude_nonactive,
                                      limit=limit, page=page, with_complexity=with_complexity,
                                      with_column_values=with_column_values, with_subitems=with_subitems,
                                      with_updates=with_updates)
        return await self.client.execute(query)

    async def get_items_by_board(self, board_ids: Union[ID, List[ID]],
                                 query_params: Optional[QueryParams] = None, limit: int = 25,
                                 cursor: str = None, with_complexity: bool = False,
                                 with_column_values: bool = True, with_subitems: bool = False,
                                 with_updates: bool = False) -> str:
        """
        Execute a query to retrieve items from a specific board, allowing filtering by IDs, sorting,
        and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

        Parameters:
            board_ids (ID): The ID of the board to retrieve items from.
            query_params (QueryParams): (Optional) A set of parameters to filter, sort,
                and control the scope of the boards query. Use this to customize the results based on specific criteria.
                Please note that you can't use query_params and cursor in the same request.
                We recommend using query_params for the initial request and cursor for paginated requests.
            limit (int): (Optional) The maximum number of items to return. Defaults to 25.
            cursor (str): An opaque cursor that represents the position in the list after the last returned item.
                Use this cursor for pagination to fetch the next set of items.
                If the cursor is null, there are no more items to fetch.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = get_items_by_board_query(board_ids=board_ids, query_params=query_params, limit=limit,
                                         cursor=cursor, with_complexity=with_complexity,
                                         with_column_values=with_column_values, with_subitems=with_subitems,
                                         with_updates=with_updates)
        return await self.client.execute(query)

    async def get_items_by_group(self, board_id: ID, group_id: ID,
                                 query_params: Optional[QueryParams] = None, limit: int = 25,
                                 cursor: str = None, with_complexity: bool = False,
                                 with_column_values: bool = True, with_subitems: bool = False,
                                 with_updates: bool = False) -> str:
        """
        Execute a query to retrieve items from a specific group within a board, allowing filtering by IDs, sorting,
        and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

        Parameters:
            board_id (ID): The ID of the board to retrieve items from.
            group_id (ID): The ID of the group to get the items by
            query_params (QueryParams): (Optional) A set of parameters to filter, sort,
                and control the scope of the boards query. Use this to customize the results based on specific criteria.
                Please note that you can't use query_params and cursor in the same request.
                We recommend using query_params for the initial request and cursor for paginated requests.
            limit (int): (Optional) The maximum number of items to return. Defaults to 25.
            cursor (str): An opaque cursor that represents the position in the list after the last returned item.
                Use this cursor for pagination to fetch the next set of items.
                If the cursor is null, there are no more items to fetch.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = get_items_by_group_query(board_id=board_id, group_id=group_id, query_params=query_params,
                                         limit=limit, cursor=cursor, with_complexity=with_complexity,
                                         with_column_values=with_column_values, with_subitems=with_subitems,
                                         with_updates=with_updates)
        return await self.client.execute(query)

    async def get_items_by_column_value(self, board_id: ID, column_id: str,
                                        column_values: Union[str, List[str]],
                                        limit: int = 25, cursor: str = None, with_complexity: bool = False,
                                        with_column_values: bool = True, with_subitems: bool = False,
                                        with_updates: bool = False) -> str:
        """
        Execute a query to retrieve items based on the value of a specific column.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

        Parameters:
            board_id (ID): The ID of the board containing the items.
            column_id (str): The unique identifier of the column to filter by.
            column_values (Union[str, List[str]]): The column value to search for.
            limit (int): (Optional) The maximum number of items to return. Defaults to 25.
            cursor (str): An opaque cursor that represents the position in the list after the last returned item.
                Use this cursor for pagination to fetch the next set of items.
                If the cursor is null, there are no more items to fetch.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = get_items_by_column_value_query(board_id=board_id, column_id=column_id,
                                                column_values=column_values, limit=limit, cursor=cursor,
                                                with_complexity=with_complexity, with_column_values=with_column_values,
                                                with_subitems=with_subitems, with_updates=with_updates)
        return await self.client.execute(query)

    async def get_items_by_multiple_column_values(self, board_id: ID,
                                                  columns: Union[ItemByColumnValuesParam, dict, List[dict]],
                                                  limit: int = 25, cursor: str = None,
                                                  with_complexity: bool = False, with_column_values: bool = True,
                                                  with_subitems: bool = False, with_updates: bool = False) -> str:
        """
        Execute a query to retrieve items based on the values of multiple columns.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

        Parameters:
            board_id (ID): The ID of the board containing the items.
            columns (Union[ItemByColumnValuesParam, dict]): The column values to filter by can be ItemByColumnValuesParam
                instance or a list consisting of dictionaries of this format:
                {"column_id": column_id, "column_values": column_values}
            limit (int): (Optional) The maximum number of items to return. Defaults to 25.
            cursor (str): An opaque cursor that represents the position in the list after the last returned item.
                Use this cursor for pagination to fetch the next set of items.
                If the cursor is null, there are no more items to fetch.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = get_items_by_multiple_column_values_query(board_id=board_id, columns=columns, limit=limit,
                                                          cursor=cursor, with_complexity=with_complexity,
                                                          with_column_values=with_column_values,
                                                          with_subitems=with_subitems, with_updates=with_updates)
        return await self.client.execute(query)

    async def next_items_page(self, cursor: str, limit: int = 500, with_complexity: bool = False,
                              with_column_values: bool = True, with_subitems: bool = False,
                              with_updates: bool = False) -> str:
        """
        Execute a query to return the next set of items that correspond with the provided cursor.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page#cursor-based-pagination-using-next_items_page

        Parameters:
            cursor (str): An opaque cursor that represents the position in the list after the last returned item.
                Use this cursor for pagination to fetch the next set of items.
                If the cursor is null, there are no more items to fetch.
            limit (int): The number of items to return. 500 by default, the maximum is 500.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_subitems (bool): Set to True to return the items subitems along with the results. False by default.
            with_updates (bool): Set to True to return the items updates along with the results. False by default.
        """
        query = next_items_page_query(cursor=cursor, limit=limit, with_complexity=with_complexity,
                                      with_column_values=with_column_values, with_subitems=with_subitems,
                                      with_updates=with_updates)
        return await self.client.execute(query)

    async def create_item(self, item_name: str, board_id: ID, group_id: Optional[str] = None,
                          column_values: Optional[dict] = None, create_labels_if_missing: bool = False,
                          with_complexity: bool = False) -> str:
        """
        Execute a query to create a new item on a specified board and group with a given name and optional column values.

        For more information, visit https://developer.monday.com/api-reference/reference/items#create-an-item

        Parameters:
            item_name (str): The name of the new item.
            board_id (ID): The ID of the board to create the item on.
            group_id (str): (Optional) The ID of the group to create the item in.
            column_values (dict): (Optional) The column values for the new item in JSON format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_item_query(item_name=item_name, board_id=board_id, group_id=group_id,
                                  column_values=column_values, create_labels_if_missing=create_labels_if_missing,
                                  with_complexity=with_complexity)
        return await self.client.execute(query)

    async def duplicate_item(self, board_id: ID, item_id: ID, with_updates: Optional[bool] = None,
                             with_complexity: bool = False) -> str:
        """
        Execute a query to create a copy of an item on the same board, with the option to include updates.

        For more information, visit https://developer.monday.com/api-reference/reference/items#duplicate-an-item

        Parameters:
            board_id (ID): The ID of the board containing the item to duplicate.
            with_updates (bool): (Optional) Whether to include the item's updates in the duplication.
            item_id (ID): The ID of the item to duplicate.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = duplicate_item_query(board_id=board_id, item_id=item_id, with_updates=with_updates,
                                     with_complexity=with_complexity)
        return await self.client.execute(query)

    async def archive_item(self, item_id: ID, with_complexity: bool = False) -> str:
        """
        Execute a query to archive an item, making it no longer visible in the active item list.

        For more information, visit https://developer.monday.com/api-reference/reference/items#archive-an-item

        Parameters:
            item_id (ID): The ID of the item to archive.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = archive_item_query(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_item(self, item_id: ID, with_complexity: bool = False) -> str:
        """
        Execute a query to permanently remove an item from a board.

        For more information, visit https://developer.monday.com/api-reference/reference/items#delete-an-item

        Parameters:
            item_id (ID): The ID of the item to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_item_query(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def get_subitems_by_parent_item(self, parent_item_id: ID,
                                          with_column_values: bool = True,
                                          with_complexity: bool = False) -> str:
        """
        Execute a query to retrieve subitems of a specific item.

        For more information, visit https://developer.monday.com/api-reference/reference/subitems#queries

        Parameters:
            parent_item_id (ID): The ID of the parent item to retrieve subitems from.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_subitems_by_parent_item_query(parent_item_id=parent_item_id,
                                                  with_column_values=with_column_values,
                                                  with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_subitem(self, parent_item_id: ID, subitem_name: str,
                             column_values: Optional[dict] = None,
                             create_labels_if_missing: bool = False,
                             with_complexity: bool = False) -> str:
        """
        Execute a query to create a new subitem under a specific parent item with a given name and optional column values.

        For more information, visit https://developer.monday.com/api-reference/reference/subitems#create-a-subitem

        Parameters:
            parent_item_id (ID): The ID of the parent item.
            subitem_name (str): The name of the new subitem.
            column_values (dict): (Optional) The column values for the new subitem in JSON format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_subitem_query(parent_item_id=parent_item_id, subitem_name=subitem_name,
                                     column_values=column_values, create_labels_if_missing=create_labels_if_missing,
                                     with_complexity=with_complexity)
        return await self.client.execute(query)

    async def change_multiple_item_column_values(self, item_id: ID, board_id: ID, column_values: dict,
                                                 create_labels_if_missing: bool = False,
                                                 with_complexity: bool = False) -> str:
        """
        Execute a query to update the values of multiple columns for a specific item.

        For more information, visit
        https://developer.monday.com/api-reference/reference/columns#change-multiple-column-values

        Parameters:
            item_id (ID): The ID of the item to update.
            board_id (ID): The ID of the board containing the item.
            column_values (dict): The updated column values as a dictionary in a {column_id: column_value, ...} format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = change_multiple_item_column_values_query(item_id=item_id, board_id=board_id,
                                                         column_values=column_values,
                                                         create_labels_if_missing=create_labels_if_missing,
                                                         with_complexity=with_complexity)
        return await self.client.execute(query)

    async def change_item_column_json_value(self, item_id: ID, column_id: str, board_id: ID, value: dict,
                                            create_labels_if_missing: bool = False,
                                            with_complexity: bool = False) -> str:
        """
        Execute a query to update the value of a specific column for an item using a JSON value.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#change-a-column-value

        Parameters:
            item_id (ID): (Optional) The ID of the item to update.
            column_id (str): The unique identifier of the column to update.
            board_id (ID): The ID of the board containing the item.
            value (dict): The new value for the column as a dictionary.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = change_item_column_json_value_query(item_id=item_id, column_id=column_id, board_id=board_id,
                                                    value=value, create_labels_if_missing=create_labels_if_missing,
                                                    with_complexity=with_complexity)
        return await self.client.execute(query)

    async def change_item_column_simple_value(self, item_id: ID, column_id: str, board_id: ID, value: str,
                                              create_labels_if_missing: bool = False,
                                              with_complexity: bool = False) -> str:
        """
        Execute a query to update the value of a specific column for an item using a simple string value.

        For more information, visit
        https://developer.monday.com/api-reference/reference/columns#change-a-simple-column-value

        Parameters:
            item_id (ID): (Optional) The ID of the item to update.
            column_id (str): The unique identifier of the column to update.
            board_id (ID): The ID of the board containing the item.
            value (str): The new simple string value for the column. Use null to clear the column value.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = change_item_column_simple_value_query(item_id=item_id, column_id=column_id, board_id=board_id,
                                                      value=value, create_labels_if_missing=create_labels_if_missing,
                                                      with_complexity=with_complexity)
        return await self.client.execute(query)

    async def upload_file_to_column(self, item_id: ID, column_id: str, file: str, with_complexity: bool = False) -> str:
        """
        Execute a query to upload a file and add it to a specific column of an item.

        For more information, visit
        https://developer.monday.com/api-reference/reference/assets-1#add-file-to-the-file-column

        Parameters:
            item_id (ID): The ID of the item to add the file to.
            column_id (str): The unique identifier of the column to add the file to.
            file (str): The filepath to the file.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = upload_file_to_column_query(item_id=item_id, column_id=column_id, with_complexity=with_complexity)
        return await self.file_upload_client.execute(query, variables={"file": file})

    async def get_item_updates(self, item_id: ID, ids: Union[ID, List[ID]] = None,
                               limit: int = 25, page: int = 1, with_complexity: bool = False) -> str:
        """
        Execute a query to retrieve updates associated with a specific item, allowing pagination and filtering by update IDs.

        Parameters:
            item_id (ID): The ID of the item to retrieve updates from.
            ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.
            limit (int): (Optional) The maximum number of updates to return. Defaults to 25.
            page (int): (Optional) The page number to return. Starts at 1.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_item_updates_query(item_id=item_id, ids=ids, limit=limit, page=page,
                                       with_complexity=with_complexity)
        return await self.client.execute(query)

    async def clear_item_updates(self, item_id: ID, with_complexity: bool = False) -> str:
        """
        Execute a query to remove all updates associated with a specific item.

        For more information, visit https://developer.monday.com/api-reference/reference/items#clear-an-items-updates

        Parameters:
            item_id (ID): The ID of the item to clear updates from.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = clear_item_updates_query(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def move_item_to_group(self, item_id: ID, group_id: str, with_complexity: bool = False) -> str:
        """
        Execute a query to move an item to a different group within the same board.

        For more information, visit https://developer.monday.com/api-reference/reference/items#move-item-to-group

        Parameters:
            item_id (ID): The ID of the item to move.
            group_id (str): The ID of the target group within the board.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = move_item_to_group_query(item_id=item_id, group_id=group_id, with_complexity=with_complexity)
        return await self.client.execute(query)
