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

from typing import Optional, Union

from monday_async.graphql.mutations import (
    archive_item_mutation,
    change_item_column_json_value_mutation,
    change_item_column_simple_value_mutation,
    change_multiple_item_column_values_mutation,
    clear_item_updates_mutation,
    create_item_mutation,
    create_subitem_mutation,
    delete_item_mutation,
    duplicate_item_mutation,
    move_item_to_board_mutation,
    move_item_to_group_mutation,
    upload_file_to_column_mutation,
)
from monday_async.graphql.queries import (
    get_item_updates_query,
    get_items_by_board_query,
    get_items_by_column_value_query,
    get_items_by_group_query,
    get_items_by_id_query,
    get_items_by_multiple_column_values_query,
    get_subitems_by_parent_item_query,
    next_items_page_query,
)
from monday_async.resources.base_resource import AsyncBaseResource
from monday_async.types import ColumnsMappingInput, ItemByColumnValuesParam, QueryParams

ID = Union[int, str]


class ItemResource(AsyncBaseResource):
    async def get_items_by_id(
        self,
        ids: ID | list[ID],
        newest_first: bool | None = None,
        exclude_nonactive: bool | None = None,
        limit: int = 25,
        page: int = 1,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve items, allowing filtering by IDs, sorting, and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items#queries

        Args:
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
        query = get_items_by_id_query(
            ids=ids,
            newest_first=newest_first,
            exclude_nonactive=exclude_nonactive,
            limit=limit,
            page=page,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def get_items_by_board(
        self,
        board_ids: ID | list[ID],
        query_params: QueryParams | None = None,
        limit: int = 25,
        cursor: Optional[str] = None,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve items from a specific board, allowing filtering by IDs, sorting,
        and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

        Args:
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
        query = get_items_by_board_query(
            board_ids=board_ids,
            query_params=query_params,
            limit=limit,
            cursor=cursor,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def get_items_by_group(
        self,
        board_id: ID,
        group_id: ID,
        query_params: QueryParams | None = None,
        limit: int = 25,
        cursor: Optional[str] = None,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve items from a specific group within a board, allowing filtering by IDs, sorting,
        and excluding inactive items.

        For more information, visit https://developer.monday.com/api-reference/reference/items-page#queries

        Args:
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
        query = get_items_by_group_query(
            board_id=board_id,
            group_id=group_id,
            query_params=query_params,
            limit=limit,
            cursor=cursor,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def get_items_by_column_value(
        self,
        board_id: ID,
        column_id: str,
        column_values: str | list[str],
        limit: int = 25,
        cursor: Optional[str] = None,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve items based on the value of a specific column.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

        Args:
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
        query = get_items_by_column_value_query(
            board_id=board_id,
            column_id=column_id,
            column_values=column_values,
            limit=limit,
            cursor=cursor,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def get_items_by_multiple_column_values(
        self,
        board_id: ID,
        columns: ItemByColumnValuesParam | dict | list[dict],
        limit: int = 25,
        cursor: Optional[str] = None,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve items based on the values of multiple columns.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page-by-column-values#queries

        Args:
            board_id (ID): The ID of the board containing the items.
            columns (Union[ItemByColumnValuesParam, dict]): The column values to filter by can be
                ItemByColumnValuesParam instance or a list consisting of dictionaries of this format:
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
        query = get_items_by_multiple_column_values_query(
            board_id=board_id,
            columns=columns,
            limit=limit,
            cursor=cursor,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def next_items_page(
        self,
        cursor: str,
        limit: int = 500,
        with_complexity: bool = False,
        with_column_values: bool = True,
        with_subitems: bool = False,
        with_updates: bool = False,
    ) -> dict:
        """
        Execute a query to return the next set of items that correspond with the provided cursor.

        For more information, visit
        https://developer.monday.com/api-reference/reference/items-page#cursor-based-pagination-using-next_items_page

        Args:
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
        query = next_items_page_query(
            cursor=cursor,
            limit=limit,
            with_complexity=with_complexity,
            with_column_values=with_column_values,
            with_subitems=with_subitems,
            with_updates=with_updates,
        )
        return await self.client.execute(query)

    async def create_item(
        self,
        item_name: str,
        board_id: ID,
        group_id: str | None = None,
        column_values: dict | None = None,
        create_labels_if_missing: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a new item on a specified board and group with a given name
        and optional column values.

        For more information, visit https://developer.monday.com/api-reference/reference/items#create-an-item

        Args:
            item_name (str): The name of the new item.
            board_id (ID): The ID of the board to create the item on.
            group_id (str): (Optional) The ID of the group to create the item in.
            column_values (dict): (Optional) The column values for the new item in JSON format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = create_item_mutation(
            item_name=item_name,
            board_id=board_id,
            group_id=group_id,
            column_values=column_values,
            create_labels_if_missing=create_labels_if_missing,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def duplicate_item(
        self, board_id: ID, item_id: ID, with_updates: bool | None = None, with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to create a copy of an item on the same board, with the option to include updates.

        For more information, visit https://developer.monday.com/api-reference/reference/items#duplicate-an-item

        Args:
            board_id (ID): The ID of the board containing the item to duplicate.
            with_updates (bool): (Optional) Whether to include the item's updates in the duplication.
            item_id (ID): The ID of the item to duplicate.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = duplicate_item_mutation(
            board_id=board_id, item_id=item_id, with_updates=with_updates, with_complexity=with_complexity
        )
        return await self.client.execute(mutation)

    async def archive_item(self, item_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to archive an item, making it no longer visible in the active item list.

        For more information, visit https://developer.monday.com/api-reference/reference/items#archive-an-item

        Args:
            item_id (ID): The ID of the item to archive.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = archive_item_mutation(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def delete_item(self, item_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to permanently remove an item from a board.

        For more information, visit https://developer.monday.com/api-reference/reference/items#delete-an-item

        Args:
            item_id (ID): The ID of the item to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = delete_item_mutation(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def get_subitems_by_parent_item(
        self, parent_item_id: ID, with_column_values: bool = True, with_complexity: bool = False
    ) -> dict:
        """
        Execute a query to retrieve subitems of a specific item.

        For more information, visit https://developer.monday.com/api-reference/reference/subitems#queries

        Args:
            parent_item_id (ID): The ID of the parent item to retrieve subitems from.
            with_column_values (bool): Set to True to return the items column values along with the results.
                True by default.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_subitems_by_parent_item_query(
            parent_item_id=parent_item_id, with_column_values=with_column_values, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def create_subitem(
        self,
        parent_item_id: ID,
        subitem_name: str,
        column_values: dict | None = None,
        create_labels_if_missing: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to create a new subitem under a specific parent item with a given name
        and optional column values.

        For more information, visit https://developer.monday.com/api-reference/reference/subitems#create-a-subitem

        Args:
            parent_item_id (ID): The ID of the parent item.
            subitem_name (str): The name of the new subitem.
            column_values (dict): (Optional) The column values for the new subitem in JSON format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = create_subitem_mutation(
            parent_item_id=parent_item_id,
            subitem_name=subitem_name,
            column_values=column_values,
            create_labels_if_missing=create_labels_if_missing,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def change_multiple_item_column_values(
        self,
        item_id: ID,
        board_id: ID,
        column_values: dict,
        create_labels_if_missing: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to update the values of multiple columns for a specific item.

        For more information, visit
        https://developer.monday.com/api-reference/reference/columns#change-multiple-column-values

        Args:
            item_id (ID): The ID of the item to update.
            board_id (ID): The ID of the board containing the item.
            column_values (dict): The updated column values as a dictionary in a {column_id: column_value, ...} format.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = change_multiple_item_column_values_mutation(
            item_id=item_id,
            board_id=board_id,
            column_values=column_values,
            create_labels_if_missing=create_labels_if_missing,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def change_item_column_json_value(
        self,
        item_id: ID,
        board_id: ID,
        column_id: str,
        value: dict,
        create_labels_if_missing: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to update the value of a specific column for an item using a JSON value.

        For more information, visit https://developer.monday.com/api-reference/reference/columns#change-a-column-value

        Args:
            item_id (ID): (Optional) The ID of the item to update.
            board_id (ID): The ID of the board containing the item.
            column_id (str): The unique identifier of the column to update.
            value (dict): The new value for the column as a dictionary.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = change_item_column_json_value_mutation(
            item_id=item_id,
            column_id=column_id,
            board_id=board_id,
            value=value,
            create_labels_if_missing=create_labels_if_missing,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def change_item_column_simple_value(
        self,
        item_id: ID,
        board_id: ID,
        column_id: str,
        value: str,
        create_labels_if_missing: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to update the value of a specific column for an item using a simple string value.

        For more information, visit
        https://developer.monday.com/api-reference/reference/columns#change-a-simple-column-value

        Args:
            item_id (ID): (Optional) The ID of the item to update.
            board_id (ID): The ID of the board containing the item.
            column_id (str): The unique identifier of the column to update.
            value (str): The new simple string value for the column. Use null to clear the column value.
            create_labels_if_missing (bool): (Optional) Whether to create missing labels for Status or Dropdown columns.
                Requires permission to change board structure.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = change_item_column_simple_value_mutation(
            item_id=item_id,
            column_id=column_id,
            board_id=board_id,
            value=value,
            create_labels_if_missing=create_labels_if_missing,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)

    async def upload_file_to_column(
        self, item_id: ID, column_id: str, file: str, with_complexity: bool = False
    ) -> dict:
        """
        Execute a mutation to upload a file and add it to a specific column of an item.

        For more information, visit
        https://developer.monday.com/api-reference/reference/assets-1#add-file-to-the-file-column

        Args:
            item_id (ID): The ID of the item to add the file to.
            column_id (str): The unique identifier of the column to add the file to.
            file (str): The filepath to the file.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = upload_file_to_column_mutation(item_id=item_id, column_id=column_id, with_complexity=with_complexity)
        return await self.file_upload_client.execute(mutation, variables={"file": file})

    async def get_item_updates(
        self,
        item_id: ID,
        ids: ID | list[ID] = None,
        limit: int = 25,
        page: int = 1,
        with_viewers: bool = False,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a query to retrieve updates associated with a specific item,
         allowing pagination and filtering by update IDs.

        Args:
            item_id (ID): The ID of the item to retrieve updates from.
            ids (Union[ID, List[ID]]): (Optional) A list of update IDs to retrieve specific updates.
            limit (int): (Optional) The maximum number of updates to return. Defaults to 25.
            page (int): (Optional) The page number to return. Starts at 1.
            with_viewers (bool): Set to True to return the viewers of the update.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_item_updates_query(
            item_id=item_id, ids=ids, limit=limit, page=page, with_viewers=with_viewers, with_complexity=with_complexity
        )
        return await self.client.execute(query)

    async def clear_item_updates(self, item_id: ID, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to remove all updates associated with a specific item.

        For more information, visit https://developer.monday.com/api-reference/reference/items#clear-an-items-updates

        Args:
            item_id (ID): The ID of the item to clear updates from.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = clear_item_updates_mutation(item_id=item_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def move_item_to_group(self, item_id: ID, group_id: str, with_complexity: bool = False) -> dict:
        """
        Execute a mutation to move an item to a different group within the same board.

        For more information, visit https://developer.monday.com/api-reference/reference/items#move-item-to-group

        Args:
            item_id (ID): The ID of the item to move.
            group_id (str): The ID of the target group within the board.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        mutation = move_item_to_group_mutation(item_id=item_id, group_id=group_id, with_complexity=with_complexity)
        return await self.client.execute(mutation)

    async def move_item_to_board(
        self,
        item_id: ID,
        board_id: ID,
        group_id: Optional[str] = None,
        columns_mapping: ColumnsMappingInput | list[dict] = None,
        subitems_columns_mapping: ColumnsMappingInput | list[dict] = None,
        with_complexity: bool = False,
    ) -> dict:
        """
        Execute a mutation to move an item to a different board.
        For more information, visit https://developer.monday.com/api-reference/reference/items#move-item-to-board

        Args:
            board_id (ID): The ID of the target board.
            group_id (str): The ID of the target group within the board.
            item_id (ID): The ID of the item to move.
            columns_mapping (Union[ColumnsMappingInput, List[Dict[str, str]]]): The object that defines
                the column mapping between the original and target board. Every column type can be mapped
                except for formula columns.
                If you omit this argument, the columns will be mapped based on the best match.
            subitems_columns_mapping (Union[ColumnsMappingInput, List[Dict[str, str]]]): The object that defines the
                subitems' column mapping between the original and target board.
                Every column type can be mapped except for formula columns.
                If you omit this argument, the columns will be mapped based on the best match.
            with_complexity (bool): Set to True to return the query's complexity along with the results.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        mutation = move_item_to_board_mutation(
            item_id=item_id,
            board_id=board_id,
            group_id=group_id,
            columns_mapping=columns_mapping,
            subitems_columns_mapping=subitems_columns_mapping,
            with_complexity=with_complexity,
        )
        return await self.client.execute(mutation)
