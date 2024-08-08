from monday_async.resources.base_resource import AsyncBaseResource
from typing import List, Union, Optional, Any
from monday_async.utils.queries import (
    get_groups_by_board_query, create_group_query, update_group_query,
    duplicate_group_query, archive_group_query, delete_group_query, GroupColors
)
from monday_async.types import PositionRelative, GroupAttributes, GroupUpdateColors


ID = Union[int, str]


class GroupResource(AsyncBaseResource):
    async def get_groups_by_board(self, board_id: ID, ids: Union[str, List[str]] = None,
                                  with_complexity: bool = False) -> dict:
        """
        Execute a query to retrieve groups associated with a specific board, with the option to filter by group IDs.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#queries

        Parameters:
            board_id (ID): The ID of the board to retrieve groups from.
            ids (Union[ID, List[ID]]): (Optional) A list of group IDs to retrieve specific groups.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = get_groups_by_board_query(board_id=board_id, ids=ids, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def create_group(self, board_id: ID, group_name: str, group_color: Optional[Union[GroupColors, str]] = None,
                           relative_to: Optional[str] = None,
                           position_relative_method: Optional[PositionRelative] = None,
                           with_complexity: bool = False) -> dict:
        """
        Execute a query to create a new group on a specific board with a specified name and positioning relative to other groups.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#create-a-group

        Parameters:
            board_id (ID): The ID of the board to create the group on.
            group_name (str): The name of the new group.
            group_color (Optional[Union[GroupColors, str]]): The group's color. Pass as a HEX value when passing as a string
                For some reason currently not all colors work.
            relative_to (str): (Optional) The ID of the group to position the new group relative to.
            position_relative_method (PositionRelative): (Optional) The method for positioning the new group:
                before_at or after_at.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = create_group_query(board_id=board_id, group_name=group_name, group_color=group_color,
                                   relative_to=relative_to, position_relative_method=position_relative_method,
                                   with_complexity=with_complexity)
        return await self.client.execute(query)

    async def update_group(self, board_id: ID, group_id: str,
                           group_attribute: GroupAttributes,
                           new_value: Union[Any, GroupUpdateColors],
                           with_complexity: bool = False) -> dict:
        """
        Execute a query to modify an existing group's title, color, or position on the board.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#update-a-group

        Parameters:
            board_id (ID): The ID of the board containing the group.
            group_id (str): The unique identifier of the group to update.
            group_attribute (GroupAttributes): The attribute of the group to update: title, color,
                relative_position_after, or relative_position_before.
            new_value (str): The new value for the specified group attribute.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = update_group_query(board_id=board_id, group_id=group_id, group_attribute=group_attribute,
                                   new_value=new_value, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def duplicate_group(self, board_id: ID, group_id: str,
                              add_to_top: Optional[bool] = None, group_title: Optional[str] = None,
                              with_complexity: bool = False) -> dict:
        """
        Execute a query to create a copy of a group within the same board,
        with options to position the new group and set its title.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#duplicate-group

        Parameters:
            board_id (ID): The ID of the board containing the group to duplicate.
            group_id (str): The unique identifier of the group to duplicate.
            add_to_top (bool): (Optional) Whether to add the new group to the top of the board.
            group_title (str): (Optional) The title for the new duplicated group.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = duplicate_group_query(board_id=board_id, group_id=group_id, add_to_top=add_to_top,
                                      group_title=group_title, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def archive_group(self, board_id: ID, group_id: str,
                            with_complexity: bool = False) -> dict:
        """
        Execute a query to archive a group on a specific board, removing it from the active view.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#archive-a-group

        Parameters:
            board_id (ID): The ID of the board containing the group.
            group_id (str): The unique identifier of the group to archive.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = archive_group_query(board_id=board_id, group_id=group_id, with_complexity=with_complexity)
        return await self.client.execute(query)

    async def delete_group(self, board_id: ID, group_id: str,
                           with_complexity: bool = False) -> dict:
        """
        Execute a query to permanently remove a group from a board.

        For more information, visit https://developer.monday.com/api-reference/reference/groups#delete-a-group

        Parameters:
            board_id (ID): The ID of the board containing the group.
            group_id (str): The unique identifier of the group to delete.
            with_complexity (bool): Set to True to return the query's complexity along with the results.
        """
        query = delete_group_query(board_id=board_id, group_id=group_id, with_complexity=with_complexity)
        return await self.client.execute(query)
