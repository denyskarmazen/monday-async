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


from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID


def create_update_mutation(body: str, item_id: ID, parent_id: ID | None = None, with_complexity: bool = False) -> str:
    """
    This mutation creates a new update on a specific item or as a reply to another update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#create-an-update

    Args:
        body (str): The text content of the update as a string or in HTML format.
        item_id (ID): The ID of the item to create the update on.
        parent_id (Optional[ID]): The ID of the parent update to reply to.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        create_update (
            body: {format_param_value(body)},
            item_id: {format_param_value(item_id)},
            parent_id: {format_param_value(parent_id)}
        ) {{
            id
            body
            item_id
        }}
    }}
    """
    return graphql_parse(mutation)


def edit_update_mutation(update_id: ID, body: str, with_complexity: bool = False) -> str:
    """
    This mutation allows you to edit an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#edit-an-update

    Args:
        update_id (ID): The ID of the update to edit.
        body (str): The new text content of the update as a string or in HTML format.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        edit_update (
            id: {format_param_value(update_id)},
            body: {format_param_value(body)}
        ) {{
            id
            body
        }}
    }}
    """
    return graphql_parse(mutation)


def pin_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation pins an update to the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#pin-an-update
    Args:
        update_id (ID): The ID of the update to pin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        pin_to_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
            pinned_to_top {{
                item_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def unpin_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation unpins an update from the top of the updates section of a specific item. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unpin-an-update
    Args:
        update_id (ID): The ID of the update to unpin.
        with_complexity (bool): Set to True to return the query's complexity along with the results.

    Returns:
        str: The formatted GraphQL query.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unpin_from_top (
            id: {format_param_value(update_id)}
        ) {{
            id
            item_id
            pinned_to_top {{
                item_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def like_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation adds a like to a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#like-an-update

    Args:
        update_id (ID): The ID of the update to like.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        like_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def unlike_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation removes a like from a specific update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#unlike-an-update

    Args:
        update_id (ID): The ID of the update to unlike.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        unlike_update (update_id: {format_param_value(update_id)}) {{
            id
            item_id
            likes {{
                id
                reaction_type
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def delete_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation removes an update. For more information, visit
    https://developer.monday.com/api-reference/reference/updates#delete-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        delete_update (id: {format_param_value(update_id)}) {{
            id
        }}
    }}
    """
    return graphql_parse(mutation)


def add_file_to_update_mutation(update_id: ID, with_complexity: bool = False) -> str:
    """
    This mutation adds a file to an update. For more information, visit
    https://developer.monday.com/api-reference/reference/assets-1#add-a-file-to-an-update

    Args:
        update_id (ID): The unique identifier of the update to delete.
        with_complexity (bool): Set to True to return the query's complexity along with the results.
    """

    mutation = f"""
    mutation ($file: File!){{{add_complexity() if with_complexity else ""}
        add_file_to_update (update_id: {format_param_value(update_id)}, file: $file) {{
            id
            name
            url
            created_at
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = [
    "add_file_to_update_mutation",
    "create_update_mutation",
    "delete_update_mutation",
    "edit_update_mutation",
    "like_update_mutation",
    "pin_update_mutation",
    "unlike_update_mutation",
    "unpin_update_mutation",
]
