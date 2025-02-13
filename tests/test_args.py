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

import pytest

from monday_async.types.args import QueryParams, ItemByColumnValuesParam, ColumnsMappingInput
from monday_async.types.enum_values import ItemsQueryRuleOperator


# Test QueryParams
def test_query_params_empty():
    params = QueryParams()
    assert str(params) == "{rules: [], operator: and}"


def test_query_params_with_order_by():
    params = QueryParams(order_by={"column_id": "status", "direction": "asc"})
    assert 'order_by: {column_id: "status", direction: asc}' in str(params)


def test_query_params_with_ids():
    params = QueryParams(ids=[1, 2, 3])
    assert 'ids: [1, 2, 3]' in str(params)


def test_query_params_add_single_rule():
    params = QueryParams()
    params.add_rule("status", ["done", "working"], ItemsQueryRuleOperator.ANY_OF)
    expected_rule = (
        '{column_id: "status", compare_value: ["done", "working"], operator: any_of}'
    )
    assert expected_rule in str(params)


def test_query_params_single_rule_with_compare_attribute():
    params = QueryParams()
    params.add_rule("timeline", ["2023-06-30", "2023-07-01"], operator=ItemsQueryRuleOperator.BETWEEN,
                    compare_attribute="START_DATE")
    expected_rule = (
        '{column_id: "timeline", compare_value: ["2023-06-30", "2023-07-01"], '
        'compare_attribute: "START_DATE", operator: between}'
    )

    assert expected_rule in str(params)


def test_query_params_multiple_rules_with_compare_attribute():
    params = QueryParams()
    params.add_rule("timeline", ["2023-06-30", "2023-07-01"], operator=ItemsQueryRuleOperator.BETWEEN,
                    compare_attribute="START_DATE")
    params.add_rule("status", ["done", "working"])
    expected_rule_1 = (
        '{column_id: "status", compare_value: ["done", "working"], operator: any_of}'
    )
    expected_rule_2 = (
        '{column_id: "timeline", compare_value: ["2023-06-30", "2023-07-01"], '
        'compare_attribute: "START_DATE", operator: between}'
    )
    assert expected_rule_1 in str(params)
    assert expected_rule_2 in str(params)


# Test ItemByColumnValuesParam
def test_item_by_column_values_add_column():
    param = ItemByColumnValuesParam()
    param.add_column("status", ["done", "working"])
    expected_value = [{"column_id": "status", "column_values": ["done", "working"]}]
    expected_string = (
        '[{column_id: "status", column_values: ["done", "working"]}]'
    )
    assert str(param) == expected_string
    assert param.value == expected_value


# Test ColumnsMappingInput
def test_columns_mapping_input_add_mapping():
    mapping = ColumnsMappingInput()
    mapping.add_mapping("source", "target")

    expected_value = [{"source": "source", "target": "target"}]
    expected_string = (
        '[{source: "source", target: "target"}]'
    )

    assert str(mapping) == expected_string
    assert mapping.value == expected_value


def test_columns_mapping_add_multiple_mappings():
    mapping = ColumnsMappingInput()
    mapping.add_mapping("source", "target")
    mapping.add_mapping("source2", "target2")

    expected_value = [
        {"source": "source", "target": "target"},
        {"source": "source2", "target": "target2"}
    ]
    expected_string1 = (
        '{source: "source", target: "target"}'
    )
    expected_string2 = (
        '{source: "source2", target: "target2"}'
    )
    assert expected_string1 in str(mapping)
    assert expected_string2 in str(mapping)
    assert mapping.value == expected_value
