from enum import Enum
from typing import Any

import pytest

from monday_async.utils.utils import monday_json_stringify, graphql_parse, format_param_value, format_dict_value


class EnumForTesting(Enum):
    PENDING = "pending"
    COMPLETED = "completed"


# Test cases for monday_json_stringify
@pytest.mark.parametrize(
    "value, expected_output",
    [
        # Simple cases
        ({"label": "Done"}, '"{\\"label\\":\\"Done\\"}"'),
        ({"label": "Done", "status": "Completed"}, '"{\\"label\\":\\"Done\\",\\"status\\":\\"Completed\\"}"'),

        # Special characters and emojis
        ({"emoji": "😊🌟🎉"}, '"{\\"emoji\\":\\"😊🌟🎉\\"}"'),
        ({"symbols": "!@#$%^&*()_+"}, '"{\\"symbols\\":\\"!@#$%^&*()_+\\"}"'),

        # Non-Latin scripts
        ({"cyrillic": "Привет мир"}, '"{\\"cyrillic\\":\\"Привет мир\\"}"'),
        ({"japanese": "日本語"}, '"{\\"japanese\\":\\"日本語\\"}"'),

        # Nested structures
        (
                {"nested": {"key": "Value with 😊", "num": 42}},
                '"{\\"nested\\":{\\"key\\":\\"Value with 😊\\",\\"num\\":42}}"'
        ),

        # Edge cases
        (None, 'null'),
        ({}, '"{}"'),
        ({"empty": ""}, '"{\\"empty\\":\\"\\"}"'),
        ({"numbers": 123}, '"{\\"numbers\\":123}"'),
        ({"special_chars": "áéíóú"}, '"{\\"special_chars\\":\\"áéíóú\\"}"'),
    ],
    ids=[
        "simple_dict",
        "multi_key_dict",
        "emojis",
        "special_symbols",
        "cyrillic_text",
        "japanese",
        "nested_objects",
        "null_case",
        "empty_dict",
        "empty_string_value",
        "numeric_value",
        "accented_chars"
    ]
)
def test_monday_json_stringify(value, expected_output):
    assert monday_json_stringify(value) == expected_output


# Test cases for graphql_parse
@pytest.mark.parametrize(
    "query, expected",
    [
        ("query { items { id } }", "{\n  items {\n    id\n  }\n}"),
        ("query($id: ID!) {items(ids: [$id]) { name } }",
         "query ($id: ID!) {\n  items(ids: [$id]) {\n    name\n  }\n}"),
        ("mutation { create_item (board_id: 123, item_name: \"Test\") { id } }",
         "mutation {\n  create_item(board_id: 123, item_name: \"Test\") {\n    id\n  }\n}"),
        ("\n\nquery\n($id: ID!\n\t) \t\t\t{items(ids: [$id]) { name \tid} }",
         "query ($id: ID!) {\n  items(ids: [$id]) {\n    name\n    id\n  }\n}")
    ],
    ids=["simple_query", "query_with_variables", "mutation", "normalize_whitespace"]
)
def test_graphql_parse_valid_queries(query, expected):
    """Test that valid GraphQL queries are properly formatted"""
    assert graphql_parse(query) == expected


# Test cases for format_param_value
@pytest.mark.parametrize(
    "value,expected",
    [
        (EnumForTesting.PENDING, "pending"),
        (123, "123"),
        ("test", "\"test\""),
        (True, "true"),
        (None, "null"),
        (["a", 1], "[\"a\", 1]"),
        ({"key": "value"}, "{\"key\": \"value\"}"),
        (3.14, "3.14")
    ],
    ids=[
        "enum",
        "int",
        "str",
        "bool",
        "none",
        "list",
        "dict",
        "float"
    ]
)
def test_format_param_value(value: Any, expected: str):
    """Test various value types formatting"""
    assert format_param_value(value) == expected


# Test cases for format_dict_value

@pytest.mark.parametrize(
    "input_dict,expected",
    [
        ({"status": EnumForTesting.PENDING, "count": 5}, "{status: pending, count: 5}"),
        ({}, "{}"),
        ({"name": "Alice", "age": 30}, "{name: \"Alice\", age: 30}"),
        ({"nested": {"key": "value"}}, "{nested: {\"key\": \"value\"}}"),
        ({"special_chars": "áéíóú"}, "{special_chars: \"áéíóú\"}"),
        ({"emoji": "😊"}, "{emoji: \"😊\"}"),
    ],
    ids=[
        "enum_value",
        "empty_dict",
        "simple_key_value",
        "nested_dict",
        "special_chars",
        "emoji"
    ]
)
def test_format_dict_value(input_dict: dict, expected: str):
    """Test dictionary formatting with various value types"""
    assert format_dict_value(input_dict) == expected
