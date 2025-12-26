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

from monday_async.exceptions import (
    APITemporarilyBlockedError,
    BadRequestError,
    ColumnValueError,
    ComplexityError,
    ConcurrencyLimitExceededError,
    CorrectedValueError,
    CreateBoardError,
    DailyLimitExceededError,
    DeleteLastGroupError,
    DepthLimitExceededError,
    FieldLimitExceededError,
    GraphQLValidationError,
    InternalServerError,
    InvalidArgumentError,
    InvalidBoardIdError,
    InvalidColumnIdError,
    InvalidInputError,
    InvalidItemIdError,
    InvalidUserIdError,
    InvalidVersionError,
    IpRestrictedError,
    ItemNameTooLongError,
    ItemsLimitationError,
    JsonParseError,
    MaxComplexityExceededError,
    MissingRequiredPermissionsError,
    MondayAPIError,
    MultipleErrors,
    ParseError,
    RateLimitExceededError,
    RecordValidError,
    ResourceNotFoundError,
    UnauthorizedError,
    UserUnauthorizedError,
)

# Mapping of error codes returned by monday.com to exception classes
ERROR_CODES_MAPPING = {
    "INTERNAL_SERVER_ERROR": InternalServerError,
    "GRAPHQL_VALIDATION_FAILED": GraphQLValidationError,
    "API_TEMPORARILY_BLOCKED": APITemporarilyBlockedError,
    "DAILY_LIMIT_EXCEEDED": DailyLimitExceededError,
    "MAX_CONCURRENCY_EXCEEDED": ConcurrencyLimitExceededError,
    "maxConcurrencyExceeded": ConcurrencyLimitExceededError,
    "maxDepthExceeded": DepthLimitExceededError,
    "RateLimitExceeded": RateLimitExceededError,
    "IpRestricted": IpRestrictedError,
    "Unauthorized": UnauthorizedError,
    "BadRequest": BadRequestError,
    "missingRequiredPermissions": MissingRequiredPermissionsError,
    "ParseError": ParseError,
    "ColumnValueException": ColumnValueError,
    "COMPLEXITY_BUDGET_EXHAUSTED": ComplexityError,
    "maxComplexityExceeded": MaxComplexityExceededError,
    "CorrectedValueException": CorrectedValueError,
    "CreateBoardException": CreateBoardError,
    "DeleteLastGroupException": DeleteLastGroupError,
    "FIELD_LIMIT_EXCEEDED": FieldLimitExceededError,
    "InvalidArgumentException": InvalidArgumentError,
    "InvalidItemIdException": InvalidItemIdError,
    "InvalidBoardIdException": InvalidBoardIdError,
    "InvalidColumnIdException": InvalidColumnIdError,
    "InvalidUserIdException": InvalidUserIdError,
    "InvalidInputError": InvalidInputError,
    "InvalidVersionException": InvalidVersionError,
    "ItemNameTooLongException": ItemNameTooLongError,
    "ItemsLimitationException": ItemsLimitationError,
    "JsonParseException": JsonParseError,
    "RecordValidException": RecordValidError,
    "ResourceNotFoundException": ResourceNotFoundError,
    "UserUnauthorizedException": UserUnauthorizedError,
}


class ErrorParser:
    def __init__(self, response: dict, query: str):
        self.response = response
        self.query = query
        self.query_lines = query.split("\n") if query else []
        self.data = response.get("data")
        self.raw_errors = response.get("errors", [])

    def handle_errors(self):
        """Process errors and raise the appropriate exception."""
        parsed_errors = [self._parse_error(e) for e in self.raw_errors]
        error_objs = [self._create_error_instance(p) for p in parsed_errors]

        if len(error_objs) == 1:
            raise error_objs[0]

        raise MultipleErrors(
            message=self._format_multiple_errors(parsed_errors), errors=error_objs, partial_data=self.data
        )

    def _parse_error(self, error: dict) -> dict:
        """Parse a raw error into a structured dictionary with formatting context."""
        extensions = error.get("extensions", {})
        return {
            "message": error.get("message", "An error occurred, but no message was provided."),
            "locations": self._parse_locations(error.get("locations", [])),
            "path": error.get("path", []),
            "error_code": extensions.get("code"),
            "status_code": extensions.get("status_code"),
            "error_data": extensions.get("error_data", {}),
            "extensions": extensions,
            "formatted_message": None,  # To be populated later.
        }

    def _parse_locations(self, locations: list) -> list:
        """Enrich each location with surrounding query context."""
        return [self._create_location(loc) for loc in locations]

    def _create_location(self, location: dict) -> dict:
        """Build location context (previous, current, and next lines)."""
        line = location.get("line")
        if line is None:
            return {"line": None, "column": location.get("column"), "prev_line": "", "error_line": "", "next_line": ""}
        return {
            "line": line,
            "column": location.get("column"),
            "prev_line": self._get_line(line - 1),
            "error_line": self._get_line(line),
            "next_line": self._get_line(line + 1),
        }

    def _get_line(self, line_number: int) -> str:
        """Return the formatted code line from the query (or empty if out of range)."""
        if 1 <= line_number <= len(self.query_lines):
            return f"{line_number}) {self.query_lines[line_number - 1]}"
        return ""

    def _create_error_instance(self, parsed_error: dict) -> MondayAPIError:
        """Instantiate an exception object from the parsed error data."""
        parsed_error["formatted_message"] = self._format_single_error(parsed_error)
        error_class = ERROR_CODES_MAPPING.get(parsed_error["error_code"], MondayAPIError)
        return error_class(
            message=parsed_error["formatted_message"],
            error_code=parsed_error["error_code"],
            status_code=parsed_error["status_code"],
            error_data=parsed_error["error_data"],
            extensions=parsed_error["extensions"],
            path=parsed_error["path"],
            partial_data=self.data,
        )

    def _format_single_error(self, parsed_error: dict) -> str:
        """
        Build a detailed error message for a single error,
        including context from the query and error metadata.
        """
        parts = [parsed_error["message"]]
        for loc in parsed_error["locations"]:
            parts.append(self._format_location(loc))
        if parsed_error["error_code"]:
            parts.append(f" - Error Code: {parsed_error['error_code']}")
        if parsed_error["status_code"]:
            parts.append(f" - Status Code: {parsed_error['status_code']}")
        return "\n".join(parts)

    @staticmethod
    def _format_location(location: dict) -> str:
        """
        Format a location by including its line, column, and surrounding code context,
        with a caret (^) indicating the error position.
        """
        if not location.get("line"):
            return ""
        col = location.get("column", 0)
        # Compute caret with a left offset: add 2 extra spaces to account for the line number and ") " prefix.
        caret = " " * (col + 2) + "^"
        lines = []
        if location.get("prev_line"):
            lines.append(f"    {location['prev_line']}")
        if location.get("error_line"):
            lines.append(f"    {location['error_line']}")
            lines.append(f"    {caret}")
        if location.get("next_line"):
            lines.append(f"    {location['next_line']}")
        # Only add a newline after the "Location:" header if there are context lines.
        if lines:
            return f"Location: Line {location['line']}, Column {col}\n" + "\n".join(lines)
        else:
            return f"Location: Line {location['line']}, Column {col}"

    @staticmethod
    def _format_multiple_errors(parsed_errors: list) -> str:
        """
        Build a combined error message for multiple errors,
        starting with a header and concatenating each formatted error.
        """
        message_lines = ["Multiple errors occurred:"]
        for error in parsed_errors:
            # Each error already has its formatted_message.
            message_lines.append("")
            message_lines.append(error["formatted_message"])
        return "\n".join(message_lines)


class ResponseParser:
    def __init__(self, response: dict, query: str):
        self.response = response
        self.query = query
        self.data = response.get("data")
        self.raw_errors = response.get("errors")
        self._error_parser = ErrorParser(response, query)

    def parse_response(self):
        """Return the data if no errors exist; otherwise, raise the formatted exception(s)."""
        if self.raw_errors:
            self._error_parser.handle_errors()
        return self.response

    @staticmethod
    def _throw_on_error(response: dict, query: str):
        """
        Static method that processes the response and immediately raises an error
        if one (or more) errors are found.
        """
        ErrorParser(response, query).handle_errors()
