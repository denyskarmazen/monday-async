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

"""
These are the types that are used as arguments for queries
"""

import re
from typing import Any

from monday_async.core.helpers import format_dict_value, format_param_value
from monday_async.types.enum_values import ID, ItemsQueryOperator, ItemsQueryRuleOperator

# Date format pattern for YYYY-MM-DD validation
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Arg:
    """
    Base class for all query argument types.
    """

    pass


class QueryParams(Arg):
    """
    A class to create an ItemsQuery type that can be used as an argument for the items_page object
    and contains a set of parameters to filter, sort, and control the scope of the boards query.
    For more information visit https://developer.monday.com/api-reference/reference/other-types#items-query
    Args:
        ids (ID): The specific item IDs to return. The maximum is 100.

        operator (ItemsQueryOperator): The conditions between query rules. The default is and.

        order_by (Optional[Dict]): The attributes to sort results by. For more information visit
            https://developer.monday.com/api-reference/reference/other-types#itemsqueryorderby
    """

    def __init__(
        self,
        ids: ID | list[ID] | None = None,
        operator: ItemsQueryOperator = ItemsQueryOperator.AND.value,
        order_by: dict | None = None,
    ):
        self._ids = ids
        self._operator = operator
        self._order_by = order_by
        self._rules = []
        self._value = {"rules": "[]", "operator": self._operator}
        if self._ids:
            self._value["ids"] = format_param_value(self._ids)
        if self._order_by:
            if self._order_by.get("column_id"):
                self._order_by["column_id"] = format_param_value(self._order_by.get("column_id"))
                self._value["order_by"] = str(self._order_by).replace("'", "")

    def __str__(self):
        return self.format_value()

    def format_value(self) -> str:
        items = [f"{key}: {value}" for key, value in self._value.items()]
        return "{" + ", ".join(items) + "}"

    def add_rule(
        self,
        column_id: str,
        compare_value: Any,
        operator: ItemsQueryRuleOperator = ItemsQueryRuleOperator.ANY_OF,
        compare_attribute: str | None = None,
    ):
        """
        Adds a rule to the query parameters.

        Args:
            column_id (str): The unique identifier of the column to filter by.
            compare_value (Any): The column value to filter by.
                This can be a string or index value depending on the column type.
            operator (ItemsQueryRuleOperator): The condition for value comparison. Default is any_of.
            compare_attribute (Optional[str]): The comparison attribute. Most columns don't have a compare_attribute.
        """
        rule = f"{{column_id: {format_param_value(column_id)}"
        rule += f", compare_value: {format_param_value(compare_value)}"
        rule += f", compare_attribute: {format_param_value(compare_attribute)}" if compare_attribute else ""
        rule += f", operator: {operator.value if isinstance(operator, ItemsQueryRuleOperator) else operator}}}"
        self._rules.append(rule)
        self._value["rules"] = "[" + ", ".join(self._rules) + "]"


class ItemByColumnValuesParam(Arg):
    """
    A class to create a ItemsPageByColumnValuesQuery type that can be used as an argument for the
    items_page_by_column_values object and contains a set of fields used to specify which columns and column values to
    filter your results by. For more information visit
    https://developer.monday.com/api-reference/reference/other-types#items-page-by-column-values-query
    """

    def __init__(self):
        self.value: list[dict] = []

    def __str__(self):
        return f"[{', '.join(format_dict_value(column) for column in self.value)}]"

    def add_column(self, column_id: str, column_values: str | list[str]):
        """
        Parameters:
            column_id (str): The IDs of the specific columns to return results for.

            column_values (Union[str, List[str]]): The column values to filter items by.
        """
        column = {"column_id": column_id, "column_values": column_values}
        self.value.append(column)


class ColumnsMappingInput(Arg):
    """
    When using this argument, you must specify the mapping for all columns.
    You can select the target as None for any columns you don't want to map, but doing so will lose the column's data.
    For more information visit https://developer.monday.com/api-reference/reference/other-types#column-mapping-input
    """

    def __init__(self):
        self.value = []

    def add_mapping(self, source: str, target: str | None = None):
        """Adds a single mapping to the list with formatted source and target values."""
        self.value.append({"source": source, "target": target})

    def __str__(self):
        """Returns the formatted mapping string for GraphQL queries."""
        return f"[{', '.join(format_dict_value(mapping) for mapping in self.value)}]"

    def __repr__(self):
        """Provides a representation with raw mappings."""
        return f"ColumnsMappingInput(mappings={self.value})"


class UserAttributesInput(Arg):
    """
    Input type for the update_multiple_users mutation.

    This class represents the user attributes that can be updated via the API.
    All fields are optional - only specify the fields you want to update.

    For more information visit:
    https://developer.monday.com/api-reference/reference/users#update-multiple-users

    Args:
        birthday: The user's birthday in YYYY-MM-DD format.
        department: The user's department.
        email: The user's email address.
        join_date: The user's join date in YYYY-MM-DD format.
        location: The user's location.
        mobile_phone: The user's mobile phone number.
        name: The user's name.
        phone: The user's phone number.
        title: The user's title.

    Raises:
        ValueError: If birthday or join_date is not in YYYY-MM-DD format.
    """

    def __init__(
        self,
        birthday: str | None = None,
        department: str | None = None,
        email: str | None = None,
        join_date: str | None = None,
        location: str | None = None,
        mobile_phone: str | None = None,
        name: str | None = None,
        phone: str | None = None,
        title: str | None = None,
    ):
        # Validate date formats
        if birthday is not None and not _DATE_PATTERN.match(birthday):
            raise ValueError(f"birthday must be in YYYY-MM-DD format, got: {birthday}")
        if join_date is not None and not _DATE_PATTERN.match(join_date):
            raise ValueError(f"join_date must be in YYYY-MM-DD format, got: {join_date}")

        self.birthday = birthday
        self.department = department
        self.email = email
        self.join_date = join_date
        self.location = location
        self.mobile_phone = mobile_phone
        self.name = name
        self.phone = phone
        self.title = title

    def __str__(self):
        return self.format_value()

    def format_value(self) -> str:
        """Formats the input as a GraphQL object string."""
        items = []
        if self.birthday is not None:
            items.append(f"birthday: {format_param_value(self.birthday)}")
        if self.department is not None:
            items.append(f"department: {format_param_value(self.department)}")
        if self.email is not None:
            items.append(f"email: {format_param_value(self.email)}")
        if self.join_date is not None:
            items.append(f"join_date: {format_param_value(self.join_date)}")
        if self.location is not None:
            items.append(f"location: {format_param_value(self.location)}")
        if self.mobile_phone is not None:
            items.append(f"mobile_phone: {format_param_value(self.mobile_phone)}")
        if self.name is not None:
            items.append(f"name: {format_param_value(self.name)}")
        if self.phone is not None:
            items.append(f"phone: {format_param_value(self.phone)}")
        if self.title is not None:
            items.append(f"title: {format_param_value(self.title)}")
        return "{" + ", ".join(items) + "}"


__all__ = ["ColumnsMappingInput", "ItemByColumnValuesParam", "QueryParams", "UserAttributesInput"]
