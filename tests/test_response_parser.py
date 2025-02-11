import pytest

from monday_async.exceptions import *
from monday_async.utils.response_parser import ErrorParser, ResponseParser
from monday_async.utils.utils import graphql_parse


@pytest.fixture
def parsed_query():
    return graphql_parse("""query {
        items(ids: [123]) {
            id
            name
        }
    }""")


@pytest.fixture
def sample_response():
    return {}


def create_error(code=None, message="Error message", line=2, column=5, status_code=None):
    error = {
        "message": message,
        "locations": [{"line": line, "column": column}],
        "extensions": {}
    }
    if code:
        error["extensions"]["code"] = code
    if status_code:
        error["extensions"]["status_code"] = status_code
    return error


def test_single_mapped_error(parsed_query):
    response = {
        "errors": [create_error(code="Unauthorized", message="Access denied", status_code=403)]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(UnauthorizedError) as exc_info:
        parser.handle_errors()

    assert "Access denied" in str(exc_info.value), "Error message should contain 'Access denied'"
    assert exc_info.value.error_code == "Unauthorized", "Should map to UnauthorizedError class"
    assert exc_info.value.status_code == 403, "Should preserve HTTP status code from response"
    assert "Line 2, Column 5" in str(exc_info.value), "Should include location information in error message"


def test_multiple_errors(parsed_query):
    response = {
        "errors": [
            create_error(code="BadRequest"),
            create_error(code="RateLimitExceeded")
        ]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(MultipleErrors) as exc_info:
        parser.handle_errors()

    assert len(exc_info.value.errors) == 2, "Should aggregate all errors from response"
    assert isinstance(exc_info.value.errors[0], BadRequestError), "First error should be BadRequestError"
    assert isinstance(exc_info.value.errors[1], RateLimitExceededError), "Second error should be RateLimitExceededError"


def test_unmapped_error_code(parsed_query):
    response = {
        "errors": [create_error(code="ThisErrorWillNeverExistException")]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(MondayAPIError) as exc_info:
        parser.handle_errors()

    assert exc_info.value.error_code == "ThisErrorWillNeverExistException", "Should preserve unmapped error code"
    assert "Error message" in str(exc_info.value), "Should include base error message for unknown error types"


def test_error_location_formatting(parsed_query):
    response = {
        "errors": [create_error(line=2, column=10)]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(MondayAPIError) as exc_info:
        parser.handle_errors()

    error_str = str(exc_info.value)
    assert "2)   items(ids: [123]) {" in error_str, "Should show error line with line number"
    assert "            ^" in error_str, "Should indicate error column with caret symbol"
    assert "Location: Line 2, Column 10" in error_str, "Should display formal location header"


def test_missing_error_locations(parsed_query):
    response = {
        "errors": [{
            "message": "Error with no location",
            "extensions": {"code": "INTERNAL_SERVER_ERROR", "status_code": 500}
        }]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(InternalServerError) as exc_info:
        parser.handle_errors()

    expected_message = "Error with no location\n - Error Code: INTERNAL_SERVER_ERROR\n - Status Code: 500"
    assert expected_message in str(exc_info.value), "Should handle errors without location data gracefully"


def test_successful_response_parsing(sample_response):
    sample_response["data"] = {"items": [{"id": 123}]}
    parser = ResponseParser(sample_response, "")
    result = parser.parse_response()
    assert result == sample_response, "Successful response should pass through unchanged"


def test_response_parser_error_propagation(sample_response, parsed_query):
    sample_response["errors"] = [create_error(code="InvalidItemIdException")]
    parser = ResponseParser(sample_response, parsed_query)
    with pytest.raises(InvalidItemIdError) as exc_info:
        parser.parse_response()

    assert "InvalidItemIdException" in str(exc_info.value), "ResponseParser should propagate specific error types"


def test_missing_error_code(parsed_query):
    response = {
        "errors": [create_error(message="Generic error")]
    }

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(MondayAPIError) as exc_info:
        parser.handle_errors()

    assert exc_info.value.error_code is None, "Should handle errors without error codes"
    assert "Generic error" in str(exc_info.value), "Should preserve message for errors without code"


def test_complex_error_data(parsed_query):
    error = create_error(code="ColumnValueException")
    error["extensions"]["error_data"] = {"column_id": "status", "value": "invalid"}
    response = {"errors": [error]}

    parser = ErrorParser(response, parsed_query)
    with pytest.raises(ColumnValueError) as exc_info:
        parser.handle_errors()

    assert exc_info.value.error_data == {"column_id": "status",
                                         "value": "invalid"}, "Should preserve complex error data structures"
