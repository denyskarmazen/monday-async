"""
These are the types that are used as arguments for queries
"""
from typing import List, Union, Optional, Dict, Any

from monday_async.types import ItemsQueryOperator, ID, ItemsQueryRuleOperator
from monday_async.utils.utils import format_param_value, format_dict_value


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

    def __init__(self, ids: Optional[Union[ID, List[ID]]] = None,
                 operator: ItemsQueryOperator = ItemsQueryOperator.AND.value, order_by: Optional[Dict] = None):
        self._ids = ids
        self._operator = operator
        self._order_by = order_by
        self._rules = []
        self._value = {'rules': "[]", 'operator': self._operator}
        if self._ids:
            self._value['ids'] = format_param_value(self._ids)
        if self._order_by:
            if self._order_by.get('column_id'):
                self._order_by['column_id'] = format_param_value(self._order_by.get('column_id'))
                self._value['order_by'] = str(self._order_by).replace("'", "")

    def __str__(self):
        return self.format_value()

    def format_value(self) -> str:
        items = [f"{key}: {value}" for key, value in self._value.items()]
        return "{" + ", ".join(items) + "}"

    def add_rule(self, column_id: str, compare_value: Any,
                 operator: ItemsQueryRuleOperator = ItemsQueryRuleOperator.ANY_OF,
                 compare_attribute: Optional[str] = None):
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
        self._value['rules'] = '[' + ', '.join(self._rules) + ']'


class ItemByColumnValuesParam(Arg):
    """
    A class to create a ItemsPageByColumnValuesQuery type that can be used as an argument for the
    items_page_by_column_values object and contains a set of fields used to specify which columns and column values to
    filter your results by. For more information visit
    https://developer.monday.com/api-reference/reference/other-types#items-page-by-column-values-query
    """

    def __init__(self):
        self.value: List[Dict] = []

    def __str__(self):
        return f"[{', '.join(format_dict_value(column) for column in self.value)}]"

    def add_column(self, column_id: str, column_values: Union[str, List[str]]):
        """
        Parameters:
            column_id (str): The IDs of the specific columns to return results for.

            column_values (Union[str, List[str]]): The column values to filter items by.
        """
        column = {'column_id': column_id, 'column_values': column_values}
        self.value.append(column)


class ColumnsMappingInput(Arg):
    """
    When using this argument, you must specify the mapping for all columns.
    You can select the target as None for any columns you don't want to map, but doing so will lose the column's data.
    For more information visit https://developer.monday.com/api-reference/reference/other-types#column-mapping-input
    """

    def __init__(self):
        self.value = []

    def add_mapping(self, source: str, target: Optional[str] = None):
        """Adds a single mapping to the list with formatted source and target values."""
        self.value.append({"source": source, "target": target})

    def __str__(self):
        """Returns the formatted mapping string for GraphQL queries."""
        return f"[{', '.join(format_dict_value(mapping) for mapping in self.value)}]"

    def __repr__(self):
        """Provides a representation with raw mappings."""
        return f"ColumnsMappingInput(mappings={self.value})"


__all__ = ["QueryParams", "ItemByColumnValuesParam", "ColumnsMappingInput"]
