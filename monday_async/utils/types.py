from enum import Enum


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


class TargetType(Enum):
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
    ALL = "all"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

