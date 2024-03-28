import json
from graphql import parse, print_ast
from enum import Enum
from typing import List, Iterable, Tuple, Any, Optional


def monday_json_stringify(value):
    """
    Double-encodes a Python object to a JSON string as required by some APIs (e.g., Monday.com).

    Example:
    Input: {"label": "Done"}
    Output: "{\"label\":\"Done\"}"  # This is a double-encoded JSON string.

    Parameters:
    - value: A Python object to be double-encoded into a JSON string.

    Returns:
    A double-encoded JSON string.
    """
    if value:
        return json.dumps(json.dumps(value))
    # If the value is None return null instead of "null"
    return json.dumps(value)


def graphql_parse(query: str):
    """
    Parses a GraphQL query string and returns a formatted string representation of the parsed query.
    Catches any GraphGL syntax errors.

    Parameters:
    - query (str): The GraphQL query string to be parsed.

    Returns:
    - str: A formatted string representation of the parsed GraphQL query.
    """
    parsed = parse(query)
    return print_ast(parsed)


def gather_params(params: Iterable[Tuple[str, Any]], excluded_params: Optional[List[str]] = None,
                  exclude_none: bool = True) -> str:
    valid_params = [f"{param}: {format_param_value(value)}" for param, value in params
                    if not ((excluded_params and param in excluded_params) or (value is None and exclude_none))]
    return ', '.join(valid_params)


def format_param_value(value: Any):
    if value is None:
        return 'null'
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, list):
        return f"[{', '.join(format_param_value(val) for val in value)}]"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, Enum):
        return value.value
    return str(value)


