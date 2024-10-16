import re
import warnings

from monday_async.utils.utils import graphql_parse


class MondayAPIError(Exception):
    """
    Base class for all errors returned by monday.com API.
    """

    def __init__(self, message: str, error_code: str = None, status_code: int = None, error_data: dict = None,
                 extensions: dict = None, path: dict = None):
        super().__init__(message)
        self.error_code: str = error_code
        self.status_code: int = status_code
        self.error_data: dict = error_data if error_data is not None else {}
        self.extensions: dict = extensions if extensions is not None else {}
        self.path: dict = path if path is not None else {}


class MondayQueryError(MondayAPIError):
    """
    Deprecated: Use MondayAPIError instead.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "MondayQueryError is deprecated and will be removed in a future version. Use MondayAPIError instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(*args, **kwargs)


class GraphQLError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GraphQLValidationError(MondayAPIError):
    """
    Raised when a GraphQL query is invalid (HTTP 400).
    This indicates that the query you are attempting to send is not valid.
    To resolve, ensure your query is properly formatted and does not contain any syntax errors.
    """

    def __init__(self, message="GraphQL query is invalid", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class InternalServerError(MondayAPIError):
    """
    Raised when an internal server error occurs (HTTP 500). This is a general error indicating something went wrong.
    Common causes include invalid arguments or malformatted JSON values.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#internal-server-error
    """

    def __init__(self, message: str = "Internal server error occurred", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ConcurrencyLimitExceededError(MondayAPIError):
    """
    Raised when the concurrency limit is exceeded (HTTP 429).
    This indicates that the maximum number of queries allowed at once has been exceeded.
    To resolve, reduce the number of concurrent queries and implement a retry mechanism.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#concurrency-limit-exceeded
    """

    def __init__(self, message: str = "Concurrency limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class FieldLimitExceededError(MondayAPIError):
    """
    Raised when there are too many requests running concurrently.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#field-limit-exceeded
    """

    def __init__(self, message="Field limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class RateLimitExceededError(MondayAPIError):
    """
    Raised when the rate limit is exceeded (HTTP 429).
    This indicates that more than 5,000 requests were made in one minute.
    To resolve, reduce the number of requests sent in one minute.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#rate-limit-exceeded
    """

    def __init__(self, message="Rate limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class IpRestrictedError(MondayAPIError):
    """
    Raised when access is restricted due to IP address restrictions (HTTP 401).
    This indicates that an account admin has restricted access from specific IP addresses.
    To resolve, confirm that your IP address is not restricted by your account admin.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#your-ip-is-restricted
    """

    def __init__(self, message="Your IP is restricted", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class UnauthorizedError(MondayAPIError):
    """
    Raised when an unauthorized access attempt is made (HTTP 401).
    This indicates that the necessary permissions are not in place to access the data.
    To resolve, ensure your API key is valid and passed in the “Authorization” header.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#unauthorized
    """

    def __init__(self, message="Unauthorized access", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class BadRequestError(MondayAPIError):
    """
    Raised when the request is malformed or incorrect (HTTP 400).
    This indicates that the structure of the query string was passed incorrectly.
    To resolve, ensure your query string is passed with the “query” key, your request is sent as a POST request with a
    JSON body, and that your query does not contain unterminated strings.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#bad-request
    """

    def __init__(self, message="Bad request", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class MissingRequiredPermissionsError(MondayAPIError):
    """
    Raised when required permissions are missing (HTTP 200).
    his indicates that the API operation has exceeded the OAuth permission scopes granted for the app.
    To resolve, review your app's permission scopes to ensure the correct ones are requested.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#missing-required-permissions
    """

    def __init__(self, message="Missing required permissions", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ParseError(MondayAPIError):
    """
    Raised when there is a parse error in the query (HTTP 200).
    This indicates that some formatting in your query string is incorrect.
    To resolve, ensure your query is a valid string and all parentheses, brackets, and curly brackets are closed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#parse-error-on
    """

    def __init__(self, message="Parse error in the query", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ColumnValueError(MondayAPIError):
    """
    Raised when there is an error with the column value formatting (HTTP 200).
    This indicates that the column value you are attempting to send in your query is of the incorrect formatting.
    To resolve, ensure the value conforms with each column’s data structure.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#columnvalueexception
    """

    def __init__(self, message="Column value formatting error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ComplexityError(MondayAPIError):
    """
    Raised when the complexity limit is exceeded (HTTP 200).
    This indicates that you have reached the complexity limit for your query.
    To resolve, add limits to your queries and only request the information you need.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#complexityexception

    Attributes:
        remaining_complexity (int or None): The remaining budget if available.
        reset_in (int or None): The time in seconds until the budget resets.
    """

    def __init__(self, message="Complexity limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        pattern = r"budget remaining (\d+) out of \d+ reset in (\d+) seconds"
        match = re.search(pattern, message)
        if match:
            self.remaining_complexity = int(match.group(1))
            self.reset_in = int(match.group(2))
        else:
            self.remaining_complexity = None
            self.reset_in = None
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class MaxComplexityExceededError(MondayAPIError):
    """
    Raised when a single query exceeds the maximum complexity limit (HTTP 200).
    """

    def __init__(self, message="Max complexity exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class CorrectedValueError(MondayAPIError):
    """
    Raised when there is an error with the value type (HTTP 200).
    This indicates that the value you are attempting to send in your query is of the wrong type.
    To resolve, ensure the column supports the type of value format being passed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#correctedvalueexception
    """

    def __init__(self, message="Incorrect value type", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class CreateBoardError(MondayAPIError):
    """
    Raised when there is an error creating a board (HTTP 200). This indicates an issue in your query to create a board.
    To resolve, ensure the template ID is valid or the board ID exists if duplicating a board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#createboardexception
    """

    def __init__(self, message="Error creating board", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class DeleteLastGroupError(MondayAPIError):
    """
    Raised when attempting to delete the last group on a board (HTTP 409).
    This indicates that the last group on a board is being deleted or archived.
    To resolve, ensure that you have at least one group on the board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#deletelastgroupexception
    """

    def __init__(self, message="Cannot delete the last group on the board", error_code=None, status_code=None,
                 error_data=None):
        super().__init__(message, error_code, status_code, error_data)


class InvalidArgumentError(MondayAPIError):
    """
    Raised when an invalid argument is passed in the query (HTTP 200).
    This indicates that the argument being passed is not valid or you've hit a pagination limit.
    To resolve, ensure there are no typos, the argument exists for the object you are querying,
    or make your result window smaller.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidargumentexception
    """

    def __init__(self, message="Invalid argument in the query", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class InvalidItemIdError(MondayAPIError):
    """
    Raised when an invalid item ID is provided (HTTP 200).
    This indicates that the item ID being passed in the query is not a valid item ID.
    To resolve, ensure the item ID exists and you have access to the item.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invaliditemidexception
    """

    def __init__(self, message="Invalid item ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)

class InvalidBoardIdError(MondayAPIError):
    """
    Raised when an invalid board ID is provided (HTTP 200).
    This indicates that the board ID being passed in the query is not a valid board ID.
    To resolve, ensure the board ID exists and you have access to the board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidboardidexception
    """

    def __init__(self, message="Invalid board ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class InvalidColumnIdError(MondayAPIError):
    """
    Raised when an invalid column ID is provided (HTTP 200).
    This indicates that the column ID being passed in the query is not a valid column ID.
    To resolve, ensure the column ID exists and you have access to the column.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidcolumnidexception
    """

    def __init__(self, message="Invalid column ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class InvalidUserIdError(MondayAPIError):
    """
    Raised when an invalid user ID is provided (HTTP 200).
    This indicates that the user ID being passed in the query is not a valid user ID.
    To resolve, ensure the user ID exists and this user is assigned to your board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invaliduseridexception
    """

    def __init__(self, message="Invalid user ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class InvalidVersionError(MondayAPIError):
    """
    Raised when an invalid API version is requested (HTTP 200).
    This indicates that the requested API version is invalid.
    To resolve, ensure that your request follows the proper format.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidversionexception
    """

    def __init__(self, message="Invalid API version", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ItemNameTooLongError(MondayAPIError):
    """
    Raised when the item name exceeds the character limit (HTTP 200).
    This indicates that the item name you have chosen has exceeded the number of characters allowed.
    To resolve, ensure your item name is between 1 and 255 characters long.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemnametoolongexception
    """

    def __init__(self, message="Item name exceeds the allowed character limit",
                 error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ItemsLimitationError(MondayAPIError):
    """
    Raised when the limit of items on a board is exceeded (HTTP 200).
    This indicates that you have exceeded the limit of items allowed for a board.
    To resolve, keep the number of items on a board below 10,000.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemslimitationexception
    """

    def __init__(self, message="Exceeded the limit of items on the board",
                 error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class JsonParseError(MondayAPIError):
    """
    Raised when there is a JSON parse error (HTTP 400). This indicates an issue interpreting the provided JSON.
    To resolve, verify all JSON is valid using a JSON validator.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#jsonparseexception
    """

    def __init__(self, message="JSON parse error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class RecordValidError(MondayAPIError):
    """
    Raised when there is a record validation error (HTTP 422). This indicates that a board has exceeded the number of
    permitted subscribers or a user/team has exceeded the board subscription limit.
    To resolve, optimize board subscribers or reduce board subscriptions.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#recordvalidexception
    """

    def __init__(self, message="Record validation error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ResourceNotFoundError(MondayAPIError):
    """
    Raised when the requested resource is not found (HTTP 200 or 404).
    This indicates that the ID you are attempting to pass in your query is invalid.
    To resolve, ensure the ID of the item, group, or board you’re querying exists.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#resourcenotfoundexception
    """

    def __init__(self, message="Resource not found", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class UserUnauthorizedError(MondayAPIError):
    """
    Raised when the user does not have the required permissions (HTTP 403).
    This indicates that the user in question does not have permission to perform the action.
    To resolve, check if the user has permission to access or edit the given resource.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#userunauthorizedexception
    """

    def __init__(self, message="User unauthorized", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None):
        super().__init__(message, error_code, status_code, error_data, extensions, path)


class ErrorInfo:
    def __init__(self, response, query):
        self.error_message = response.get('error_message', 'An error occurred')
        self.error_code = response.get('error_code')
        self.status_code = response.get('status_code')
        self.error_data = response.get('error_data', {})
        self.path = None
        self.extensions = None
        self.query_by_lines = graphql_parse(query).split("\n")
        self.errors = []
        self.process_errors(response)
        self.formatted_message = self.format_errors()

    def process_errors(self, response):
        for err in response.get('errors', []):
            if isinstance(err, str):
                self.add_error(err, self.error_code, self.status_code)
                continue

            message = err.get('message', '')
            locations = [
                self.create_location(location) for location in err.get('locations', [])
            ]
            error_code = err.get('extensions', {}).get('code')
            status_code = err.get('extensions', {}).get('status_code')
            error_data = err.get('extensions', {}).get('error_data', {})
            path = err.get('path', [])
            extensions = err.get('extensions', {})
            self.add_error(message, error_code, status_code, locations, error_data)
            if not self.error_code:
                self.error_code = error_code
            if error_code == self.error_code:
                self.extensions = extensions
                self.path = path
                self.error_data = error_data

    def create_location(self, location):
        line = location.get('line')
        column = location.get('column')
        return {
            'line': line,
            'column': column,
            'prev_line': self.get_line(line - 1),
            'error_line': self.get_line(line),
            'next_line': self.get_line(line + 1),
        }

    def get_line(self, line_number):
        if 1 <= line_number <= len(self.query_by_lines):
            return f'{line_number}) {self.query_by_lines[line_number - 1]}'
        return ""

    def add_error(self, message, error_code=None, status_code=None, locations=None, error_data=None):
        self.errors.append({
            "message": message,
            "locations": locations if locations else [],
            "error_code": error_code,
            "status_code": status_code,
            "error_data": error_data
        })

    def format_errors(self) -> str:
        if not self.errors:
            return self.format_single_error(self.error_message, self.error_code, self.status_code)

        if len(self.errors) == 1:
            return self.format_error_details(self.errors[0])

        return self.format_multiple_errors()

    @staticmethod
    def format_single_error(message, error_code, status_code) -> str:
        return (
                f"{message}\n"
                + (f"Error Code: {error_code}\n" if error_code else "")
                + (f"Status Code: {status_code}\n" if status_code else "")
        )

    def format_error_details(self, error) -> str:
        formatted_message = f"{error['message']}\n"
        for location in error['locations']:
            formatted_message += self.format_location(location)
        formatted_message += f"Error Code: {error.get('error_code')}\n" if error.get('error_code') else ""
        formatted_message += f"Status Code: {error.get('status_code')}\n" if error.get('status_code') else ""
        return formatted_message

    @staticmethod
    def format_location(location) -> str:
        caret_line = ' ' * (location['column'] + 2) + "^"  # Indent caret below the error line at the correct column
        formatted_message = (
            f"Location: Line {location['line']}, Column {location['column']}\n"
        )
        if location['error_line']:
            if location.get('prev_line'):
                formatted_message += f"       {location['prev_line']}\n"
            formatted_message += f"       {location['error_line']}\n"
            formatted_message += f"       {caret_line}\n"
            if location.get('next_line'):
                formatted_message += f"       {location['next_line']}\n"
        return formatted_message

    def format_multiple_errors(self) -> str:
        formatted_message = "\nMultiple errors occurred:\n"
        for error in self.errors:
            formatted_message += f"\n{error['message']}\n"
            for location in error['locations']:
                formatted_message += self.format_location(location)
            formatted_message += f" - Error Code: {error.get('error_code')}\n"
            formatted_message += f" - Status Code: {error.get('status_code')}\n"
        return formatted_message


# Mapping of error codes returned by monday.com to exception classes
ERROR_CODES = {
    'INTERNAL_SERVER_ERROR': InternalServerError,
    'GRAPHQL_VALIDATION_FAILED': GraphQLValidationError,
    'MaxConcurrencyExceeded': ConcurrencyLimitExceededError,
    'RateLimitExceeded': RateLimitExceededError,
    'IpRestricted': IpRestrictedError,
    'Unauthorized': UnauthorizedError,
    'BadRequest': BadRequestError,
    'missingRequiredPermissions': MissingRequiredPermissionsError,
    'ParseError': ParseError,
    'ColumnValueException': ColumnValueError,
    'ComplexityException': ComplexityError,
    'maxComplexityExceeded': MaxComplexityExceededError,
    'CorrectedValueException': CorrectedValueError,
    'CreateBoardException': CreateBoardError,
    'DeleteLastGroupException': DeleteLastGroupError,
    'FIELD_LIMIT_EXCEEDED': FieldLimitExceededError,
    'InvalidArgumentException': InvalidArgumentError,
    'InvalidItemIdException': InvalidItemIdError,
    'InvalidBoardIdException': InvalidBoardIdError,
    'InvalidColumnIdException': InvalidColumnIdError,
    'InvalidUserIdException': InvalidUserIdError,
    'InvalidVersionException': InvalidVersionError,
    'ItemNameTooLongException': ItemNameTooLongError,
    'ItemsLimitationException': ItemsLimitationError,
    'JsonParseException': JsonParseError,
    'RecordValidException': RecordValidError,
    'ResourceNotFoundException': ResourceNotFoundError,
    'UserUnauthorizedException': UserUnauthorizedError,
}
