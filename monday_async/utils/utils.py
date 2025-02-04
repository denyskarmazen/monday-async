import json
from enum import Enum
from typing import List, Iterable, Tuple, Any, Optional

from graphql import parse, print_ast


def monday_json_stringify(value: dict) -> str:
    """
    Double-encodes a Python object to a JSON string as required by some APIs (e.g., Monday.com).

    Example:
        Input: {"label": "Done"}
        Output: "{\"label\":\"Done\"}"

    Args:
        value: A Python object to be double-encoded into a JSON string.

    Returns:
        A double-encoded JSON string.
    """
    if value:
        return json.dumps(json.dumps(value, ensure_ascii=False, separators=(',', ':')), ensure_ascii=False)
    # If the value is None return null instead of "null"
    return json.dumps(value)


def graphql_parse(query: str) -> str:
    """
    Parses a GraphQL query string and returns a formatted string representation of the parsed query.
    Catches any GraphGL syntax errors.

    Args:
        query (str): The GraphQL query string to be parsed.

    Returns:
        str: A formatted string representation of the parsed GraphQL query.
    """
    parsed = parse(query)
    return print_ast(parsed)


def gather_params(params: Iterable[Tuple[str, Any]], excluded_params: Optional[List[str]] = None,
                  exclude_none: bool = True) -> str:
    valid_params = [f"{param}: {format_param_value(value)}" for param, value in params
                    if not ((excluded_params and param in excluded_params) or (value is None and exclude_none))]
    return ', '.join(valid_params)


def format_param_value(value: Any) -> str:
    if isinstance(value, Enum):
        return json.dumps(value.value)
    return json.dumps(value)


def format_dict_value(dictionary: dict) -> str:
    output = [f"{key}: {format_param_value(value)}" for key, value in dictionary.items()]
    if output:
        return f"{{{', '.join(output)}}}"
    return "{}"
