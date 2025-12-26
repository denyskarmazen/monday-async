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

from monday_async.graphql.addons import (
    add_column_values,
    add_columns,
    add_complexity,
    add_groups,
    add_subitems,
    add_updates,
)


@pytest.mark.parametrize(
    "func, required_fields",
    [
        (add_complexity, ["complexity", "before", "query", "after", "reset_in_x_seconds"]),
        (add_columns, ["columns", "id", "title", "type", "settings_str"]),
        (add_groups, ["groups", "id", "title", "color", "position"]),
        (
            add_column_values,
            [
                "column_values",
                "column",
                "title",
                "settings_str",
                "type",
                "value",
                "text",
                "... on BoardRelationValue",
                "... on CheckboxValue",
                "... on CountryValue",
                "... on DateValue",
                "... on LocationValue",
                "... on MirrorValue",
                "... on PeopleValue",
            ],
        ),
        (add_subitems, ["subitems", "id", "name", "url", "state"]),
        (add_updates, ["updates", "id", "text_body", "body", "creator_id", "assets", "replies"]),
    ],
)
def test_query_addons_functions(func, required_fields):
    """
    Parametrized test to ensure each add_* function returns a string
    containing the required GraphQL fields.
    """
    result = func()

    assert isinstance(result, str), f"{func.__name__} did not return a string."
    assert result.strip() != "", f"{func.__name__} returned an empty string."

    for field in required_fields:
        assert field in result, f"Expected '{field}' not found in output of {func.__name__}."
