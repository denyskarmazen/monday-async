from typing import List, Union, Optional, Dict
from monday_async.utils.utils import format_param_value
from monday_async.types import ItemsQueryOperator, ID, ItemsQueryRuleOperator


class QueryParams:
    """
    A class to create a ItemsQuery type that can be used as an argument for the items_page object
    and contains a set of parameters to filter, sort, and control the scope of the boards query.

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
        self.value = {'rules': self._rules, 'operator': self._operator}
        if self._order_by:
            if self._order_by.get('column_id'):
                self._order_by['column_id'] = format_param_value(self._order_by.get('column_id'))
                self.value['order_by'] = order_by

    def __str__(self):
        return str(self.value)


    def add_rule(self, column_id: str, compare_value: Union[str, int, List[int]],
                 operator: ItemsQueryRuleOperator = ItemsQueryRuleOperator.ANY_OF.value):
        """
        Parameters:
            column_id (str): The unique identifier of the column to filter by.

            compare_value (str): The column value to filter by. This can be a string or index value depending
                on the column type.

            operator (ItemsQueryRuleOperator): The condition for value comparison. The default is any_of.
        """
        if isinstance(operator, ItemsQueryRuleOperator):
            operator_value = operator.value
        else:
            operator_value = operator

        rule = {
            'column_id': format_param_value(column_id),
            'compare_value': format_param_value(compare_value),
            'operator': operator_value
        }

        self._rules.append(rule)


class ItemByColumnValuesParam:
    """
    A class to create a ItemsPageByColumnValuesQuery type that can be used as an argument for the
    items_page_by_column_values object and contains a set of fields used to specify which columns and column values to
    filter your results by. For more information visit
    https://developer.monday.com/api-reference/reference/other-types#items-page-by-column-values-query
    """

    def __init__(self):
        self.value = []

    def __str__(self):
        return str(self.value)

    def add_column(self, column_id: str, column_values: Union[str, List[str]]):
        """
        Parameters:
            column_id (str): The IDs of the specific columns to return results for.

            column_values (Union[str, List[str]]): The column values to filter items by.
        """
        column = {'column_id': column_id, 'column_values': column_values}
        self.value.append(column)
