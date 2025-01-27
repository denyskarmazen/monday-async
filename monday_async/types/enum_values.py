"""
These are the enum values from the monday.com API documentation.
"""

from enum import Enum
from typing import Union

ID = Union[int, str]


class WebhookEventType(Enum):
    CHANGE_COLUMN_VALUE = "change_column_value"
    CHANGE_STATUS_COLUMN_VALUE = "change_status_column_value"
    CHANGE_SUBITEM_COLUMN_VALUE = "change_subitem_column_value"
    CHANGE_SPECIFIC_COLUMN_VALUE = "change_specific_column_value"
    CHANGE_NAME = "change_name"
    CREATE_ITEM = "create_item"
    ITEM_ARCHIVED = "item_archived"
    ITEM_DELETED = "item_deleted"
    ITEM_MOVED_TO_ANY_GROUP = "item_moved_to_any_group"
    ITEM_MOVED_TO_SPECIFIC_GROUP = "item_moved_to_specific_group"
    ITEM_RESTORED = "item_restored"
    CREATE_SUBITEM = "create_subitem"
    CHANGE_SUBITEM_NAME = "change_subitem_name"
    MOVE_SUBITEM = "move_subitem"
    SUBITEM_ARCHIVED = "subitem_archived"
    SUBITEM_DELETED = "subitem_deleted"
    CREATE_COLUMN = "create_column"
    CREATE_UPDATE = "create_update"
    EDIT_UPDATE = "edit_update"
    DELETE_UPDATE = "delete_update"
    CREATE_SUBITEM_UPDATE = "create_subitem_update"


class NotificationTargetType(Enum):
    POST = "Post"
    PROJECT = "Project"


class UserKind(Enum):
    ALL = "all"
    NON_GUESTS = "non_guests"
    GUESTS = "guests"
    NON_PENDING = "non_pending"


class WorkspaceKind(Enum):
    OPEN = "open"
    CLOSED = "closed"


class State(Enum):
    """The state of an item, board or workspace."""
    ALL = "all"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class SubscriberKind(Enum):
    SUBSCRIBER = "subscriber"
    OWNER = "owner"


class FolderColor(Enum):
    DONE_GREEN = "DONE_GREEN"
    BRIGHT_GREEN = "BRIGHT_GREEN"
    WORKING_ORANGE = "WORKING_ORANGE"
    DARK_ORANGE = "DARK_ORANGE"
    SUNSET = "SUNSET"
    STUCK_RED = "STUCK_RED"
    DARK_RED = "DARK_RED"
    SOFIA_PINK = "SOFIA_PINK"
    LIPSTICK = "LIPSTICK"
    PURPLE = "PURPLE"
    DARK_PURPLE = "DARK_PURPLE"
    INDIGO = "INDIGO"
    BRIGHT_BLUE = "BRIGHT_BLUE"
    AQUAMARINE = "AQUAMARINE"
    CHILI_BLUE = "CHILI_BLUE"
    NULL = "NULL"


class BoardKind(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    SHARE = "share"


class BoardAttributes(Enum):
    """Used in the update_board mutation to specify the attributes to update."""
    NAME = "name"
    DESCRIPTION = "description"
    COMMUNICATION = "communication"


class DuplicateBoardType(Enum):
    """The duplication type."""
    WITH_STRUCTURE = "duplicate_board_with_structure"
    WITH_PULSES = "duplicate_board_with_pulses"
    WITH_PULSES_AND_UPDATES = "duplicate_board_with_pulses_and_updates"


class PositionRelative(Enum):
    """You can use this argument to specify if you want to create the new group above or under
    the group specified in the relative_to argument."""
    BEFORE_AT = "before_at"
    AFTER_AT = "after_at"


class ColumnType(Enum):
    AUTO_NUMBER = "auto_number"  # Number items according to their order in the group/board
    BUTTON = "button"  # Trigger actions directly from your board
    CHECKBOX = "checkbox"  # Check off items and see what's done at a glance
    COLOR_PICKER = "color_picker"  # Manage a design system using a color palette
    CONNECT_BOARDS = "board_relation"  # Link items to other boards
    COUNTRY = "country"  # Choose a country
    CREATION_LOG = "creation_log"  # Add the item's creator and creation date automatically
    DATE = "date"  # Add dates like deadlines to ensure you never drop the ball
    DEPENDENCY = "dependency"  # Set up dependencies between items in the board
    DROPDOWN = "dropdown"  # Create a dropdown list of options
    EMAIL = "email"  # Email team members and clients directly from your board
    FILE = "file"  # Add files & docs to your item
    FORMULA = "formula"  # Calculate values using other column data
    HOUR = "hour"  # Add times to manage and schedule tasks, shifts and more
    ITEM_ID = "item_id"  # Show a unique ID for each item
    LAST_UPDATED = "last_updated"  # Add the person that last updated the item and the date
    LINK = "link"  # Simply hyperlink to any website
    LOCATION = "location"  # Place multiple locations on a geographic map
    LONG_TEXT = "long_text"  # Add large amounts of text without changing column width
    MIRROR = "mirror"  # Reflect information from connected boards
    MONDAY_DOC = "doc"  # Embed monday.com docs directly in your board
    NAME = "name"  # The name of the item
    NUMBERS = "numbers"  # Add revenue, costs, time estimations and more
    PEOPLE = "people"  # Assign people to improve team work
    PHONE = "phone"  # Call your contacts directly from monday.com
    PROGRESS = "progress"  # Show progress by combining status columns in a battery
    RATING = "rating"  # Rate or rank anything visually
    STATUS = "status"  # Get an instant overview of where things stand
    TAGS = "tags"  # Add tags to categorize items across multiple boards
    TEAM = "team"  # Assign a full team to an item
    TEXT = "text"  # Add textual information e.g. addresses, names or keywords
    TIMELINE = "timeline"  # Visually see a breakdown of your team's workload by time
    TIME_TRACKING = "time_tracking"  # Easily track time spent on each item, group, and board
    VOTE = "vote"  # Vote on an item e.g. pick a new feature or a favorite lunch place
    WEEK = "week"  # Select the week on which each item should be completed
    WORLD_CLOCK = "world_clock"  # Keep track of the time anywhere in the world


class GroupAttributes(Enum):
    """Used in the update_group mutation to specify the attributes to update."""
    TITLE = "title"
    COLOR = "color"
    POSITION = "position"
    RELATIVE_POSITION_AFTER = "relative_position_after"
    RELATIVE_POSITION_BEFORE = "relative_position_before"


class GroupUpdateColors(Enum):
    """The colors available for groups when updating them."""
    DARK_GREEN = "dark-green"
    ORANGE = "orange"
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    GREY = "grey"
    DARK_BLUE = "dark-blue"
    YELLOW = "yellow"
    LIME_GREEN = "lime-green"
    PURPLE = "purple"
    DARK_PURPLE = "dark_purple"
    BROWN = "brown"
    DARK_RED = "dark-red"
    TROLLEY_GREY = "trolley-grey"
    DARK_ORANGE = "dark-orange"
    DARK_PINK = "dark-pik"
    TURQUOISE = "turquoise"
    LIGHT_PINK = "light-pink"


class GroupColors(Enum):
    """The colors available for groups when creating them."""
    DARK_GREEN = "#037f4c"
    ORANGE = "#fdab3d"
    BLUE = "#579bfc"
    RED = "#e2445c"
    GREEN = "#00c875"
    GREY = "#c4c4c4"
    TROLLEY_GREY = "#808080"
    DARK_BLUE = "#0086c0"
    LIME_GREEN = "#9cd326"
    YELLOW = "#ffcb00"
    PURPLE = "#a25ddc"
    DARK_PURPLE = "#784bdl"
    BROWN = "#7f5347"
    DARK_RED = "#bb3354"
    DARK_ORANGE = "#ff642e"
    DARK_PINK = "#ff158a"
    TURQUOISE = "#66ccff"
    LIGHT_PINK = "#ff5ac4"


class BoardsOrderBy(Enum):
    """The order in which to retrieve your boards."""
    CREATED_AT = "created_at"
    USED_AT = "used_at"


class ItemsQueryOperator(Enum):
    """The conditions between query rules. The default is and."""
    AND = "and"
    OR = "or"


class ItemsOrderByDirection(Enum):
    """The attributes to sort results by."""
    ASCENDING = "asc"
    DESCENDING = "desc"


class ItemsQueryRuleOperator(Enum):
    """The rules to filter your queries."""
    ANY_OF = "any_of"
    NOT_ANY_OF = "not_any_of"
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUALS = "greater_than_or_equals"
    LOWER_THAN = "lower_than"
    LOWER_THAN_OR_EQUAL = "lower_than_or_equal"
    BETWEEN = "between"
    NOT_CONTAINS_TEXT = "not_contains_text"
    CONTAINS_TEXT = "contains_text"
    CONTAINS_TERMS = "contains_terms"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    WITHIN_THE_NEXT = "within_the_next"
    WITHIN_THE_LAST = "within_the_last"


__all__ = [
    "WebhookEventType", "NotificationTargetType", "UserKind", "WorkspaceKind", "State", "SubscriberKind", "FolderColor",
    "BoardKind", "BoardAttributes", "DuplicateBoardType", "PositionRelative", "ColumnType", "GroupAttributes",
    "GroupUpdateColors", "GroupColors", "BoardsOrderBy", "ItemsQueryOperator", "ItemsOrderByDirection",
    "ItemsQueryRuleOperator", "ID"
]
