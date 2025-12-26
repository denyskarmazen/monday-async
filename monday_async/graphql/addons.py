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


from monday_async.core.helpers import format_param_value
from monday_async.types import ID


def add_complexity() -> str:
    """This can be added to any query to return its complexity with it"""
    query = """
        complexity {
            before
            query
            after
            reset_in_x_seconds
        }
    """
    return query


def add_columns() -> str:
    """This can be added to any boards query to return its columns with it"""
    columns = """
    columns {
        id
        title
        type
        settings_str
    }
    """
    return columns


def add_groups() -> str:
    """This can be added to any boards query to return its groups with it"""
    groups = """
    groups {
        id
        title
        color
        position
    }
    """
    return groups


def add_column_values() -> str:
    """This can be added to any items query to return its column values with it"""
    column_values = """
    column_values {
        id
        column {
            title
            settings_str
        }
        type
        text
        value
        ... on BoardRelationValue {
            display_value
            linked_item_ids
        }
        ... on CheckboxValue {
            checked
        }
        ... on CountryValue {
            country {
                name
            }
        }
        ... on DateValue {
            date
            time
        }
        ... on LocationValue {
            lat
            lng
            address
        }
        ... on MirrorValue {
            display_value
            mirrored_items {
                linked_item {
                    id
                    name
                }
            }
        }
        ... on PeopleValue {
            persons_and_teams {
                id
                kind
            }
        }
        ... on FormulaValue {
            display_value
        }
    }
    """
    return column_values


def add_subitems() -> str:
    """This can be added to any items query to return its subitems with it"""
    subitems = """
    subitems {
        id
        name
        url
        state
    }
    """
    return subitems


def add_updates(
    ids: ID | list[ID] | None = None,
    limit: int = 100,
    page: int = 1,
    with_pins: bool = False,
    with_likes: bool = False,
    with_viewers: bool = False,
) -> str:
    """
    This can be added to any items query to return its updates with it

    Args:
        ids (Union[ID, List[ID]]): A list of update IDs to retrieve specific updates.
        limit (int): the maximum number of updates to return. Defaults to 100. Maximum is 100 per page.
        page (int): The page number to return. Starts at 1.
        with_pins (bool): Set to True to return the pinned_to_top field.
        with_likes (bool): Set to True to return the likes of the update.
        with_viewers (bool): Set to True to return the viewers of the update.
    """
    viewers = """
    viewers {
        medium
        user {
            id
            name
            email
            title
        }
    }
    """
    likes = """
    likes {
        id
        reaction_type
        creator_id
        updated_at
    }
    """
    pinned = """
    pinned_to_top {
        item_id
    }
    """
    updates = f"""
    updates (ids: {format_param_value(ids if ids else None)}, limit: {limit}, page: {page}) {{
        id
        text_body
        body
        creator_id
        assets {{
            id
            name
            file_extension
            url
            public_url
        }}
        replies {{
            id
            text_body
        }}
        edited_at
        {pinned if with_pins else ""}
        {likes if with_likes else ""}
        {viewers if with_viewers else ""}
    }}
    """
    return updates


__all__ = ["add_column_values", "add_columns", "add_complexity", "add_groups", "add_subitems", "add_updates"]
