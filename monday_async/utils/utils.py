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

import json
from enum import Enum
from typing import Any

from graphql import parse, print_ast


def monday_json_stringify(value: dict) -> str:
    """
    Double-encodes a Python object to a JSON string as required by some APIs (e.g., Monday.com).

    Example:
        Input: {"label": "Done"}
        Output: '\"{\\"label\\":\\"Done\\"}\"'

    Args:
        value: A Python object to be double-encoded into a JSON string.

    Returns:
        A double-encoded JSON string.
    """
    if value is not None:
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


def format_param_value(value: Any) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    return json.dumps(value, ensure_ascii=False)


def format_dict_value(dictionary: dict) -> str:
    output = [f"{key}: {format_param_value(value)}" for key, value in dictionary.items()]
    if output:
        return f"{{{', '.join(output)}}}"
    return "{}"
