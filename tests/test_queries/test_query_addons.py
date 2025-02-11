import pytest

from monday_async.utils.queries.query_addons import (
    add_complexity,
    add_columns,
    add_groups,
    add_column_values,
    add_subitems,
    add_updates
)


@pytest.mark.parametrize(
    "func, required_fields",
    [
        (
                add_complexity,
                [
                    "complexity",
                    "before",
                    "query",
                    "after",
                    "reset_in_x_seconds"
                ]
        ),
        (
                add_columns,
                [
                    "columns",
                    "id",
                    "title",
                    "type",
                    "settings_str"
                ]
        ),
        (
                add_groups,
                [
                    "groups",
                    "id",
                    "title",
                    "color",
                    "position"
                ]
        ),
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
                ]
        ),
        (
                add_subitems,
                [
                    "subitems",
                    "id",
                    "name",
                    "url",
                    "state"
                ]
        ),
        (
                add_updates,
                [
                    "updates",
                    "id",
                    "text_body",
                    "body",
                    "creator_id",
                    "assets",
                    "replies"
                ]
        ),
    ]
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
