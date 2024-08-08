from monday_async.utils.utils import graphql_parse


class MondayQueryError(Exception):
    """
    Base class for all Monday query errors.
    """

    def __init__(self, message, original_errors=None):
        super().__init__(message)
        self.original_errors = original_errors or []


class GraphQLError(Exception):
    def __init__(self, message, original_errors=None):
        super().__init__(message)
        self.original_errors = original_errors or []


class InternalServerError(MondayQueryError):
    """
    Raised when an internal server error occurs (HTTP 500). This is a general error indicating something went wrong.
    Common causes include invalid arguments or malformatted JSON values.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#internal-server-error
    """

    def __init__(self, message="Internal server error occurred", original_errors=None):
        super().__init__(message, original_errors)


class ConcurrencyLimitExceededError(MondayQueryError):
    """
    Raised when the concurrency limit is exceeded (HTTP 429).
    This indicates that the maximum number of queries allowed at once has been exceeded.
    To resolve, reduce the number of concurrent queries and implement a retry mechanism.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#concurrency-limit-exceeded
    """

    def __init__(self, message="Concurrency limit exceeded", original_errors=None):
        super().__init__(message, original_errors)


class RateLimitExceededError(MondayQueryError):
    """
    Raised when the rate limit is exceeded (HTTP 429).
    This indicates that more than 5,000 requests were made in one minute.
    To resolve, reduce the number of requests sent in one minute.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#rate-limit-exceeded
    """

    def __init__(self, message="Rate limit exceeded", original_errors=None):
        super().__init__(message, original_errors)


class IpRestrictedError(MondayQueryError):
    """
    Raised when access is restricted due to IP address restrictions (HTTP 401).
    This indicates that an account admin has restricted access from specific IP addresses.
    To resolve, confirm that your IP address is not restricted by your account admin.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#your-ip-is-restricted
    """

    def __init__(self, message="Your IP is restricted", original_errors=None):
        super().__init__(message, original_errors)


class UnauthorizedError(MondayQueryError):
    """
    Raised when an unauthorized access attempt is made (HTTP 401).
    This indicates that the necessary permissions are not in place to access the data.
    To resolve, ensure your API key is valid and passed in the “Authorization” header.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#unauthorized
    """

    def __init__(self, message="Unauthorized access", original_errors=None):
        super().__init__(message, original_errors)


class BadRequestError(MondayQueryError):
    """
    Raised when the request is malformed or incorrect (HTTP 400).
    This indicates that the structure of the query string was passed incorrectly.
    To resolve, ensure your query string is passed with the “query” key, your request is sent as a POST request with a
    JSON body, and that your query does not contain unterminated strings.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#bad-request
    """

    def __init__(self, message="Bad request", original_errors=None):
        super().__init__(message, original_errors)


class MissingRequiredPermissionsError(MondayQueryError):
    """
    Raised when required permissions are missing (HTTP 200).
    his indicates that the API operation has exceeded the OAuth permission scopes granted for the app.
    To resolve, review your app's permission scopes to ensure the correct ones are requested.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#missing-required-permissions
    """

    def __init__(self, message="Missing required permissions", original_errors=None):
        super().__init__(message, original_errors)


class ParseError(MondayQueryError):
    """
    Raised when there is a parse error in the query (HTTP 200).
    This indicates that some formatting in your query string is incorrect.
    To resolve, ensure your query is a valid string and all parentheses, brackets, and curly brackets are closed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#parse-error-on
    """

    def __init__(self, message="Parse error in the query", original_errors=None):
        super().__init__(message, original_errors)


class ColumnValueError(MondayQueryError):
    """
    Raised when there is an error with the column value formatting (HTTP 200).
    This indicates that the column value you are attempting to send in your query is of the incorrect formatting.
    To resolve, ensure the value conforms with each column’s data structure.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#columnvalueexception
    """

    def __init__(self, message="Column value formatting error", original_errors=None):
        super().__init__(message, original_errors)


class ComplexityError(MondayQueryError):
    """
    Raised when the complexity limit is exceeded (HTTP 200).
    This indicates that you have reached the complexity limit for your query.
    To resolve, add limits to your queries and only request the information you need.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#complexityexception
    """

    def __init__(self, message="Complexity limit exceeded", original_errors=None):
        super().__init__(message, original_errors)


class CorrectedValueError(MondayQueryError):
    """
    Raised when there is an error with the value type (HTTP 200).
    This indicates that the value you are attempting to send in your query is of the wrong type.
    To resolve, ensure the column supports the type of value format being passed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#correctedvalueexception
    """

    def __init__(self, message="Incorrect value type", original_errors=None):
        super().__init__(message, original_errors)


class CreateBoardError(MondayQueryError):
    """
    Raised when there is an error creating a board (HTTP 200). This indicates an issue in your query to create a board.
    To resolve, ensure the template ID is valid or the board ID exists if duplicating a board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#createboardexception
    """

    def __init__(self, message="Error creating board", original_errors=None):
        super().__init__(message, original_errors)


class DeleteLastGroupError(MondayQueryError):
    """
    Raised when attempting to delete the last group on a board (HTTP 409).
    This indicates that the last group on a board is being deleted or archived.
    To resolve, ensure that you have at least one group on the board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#deletelastgroupexception
    """

    def __init__(self, message="Cannot delete the last group on the board", original_errors=None):
        super().__init__(message, original_errors)


class InvalidArgumentError(MondayQueryError):
    """
    Raised when an invalid argument is passed in the query (HTTP 200).
    This indicates that the argument being passed is not valid or you've hit a pagination limit.
    To resolve, ensure there are no typos, the argument exists for the object you are querying,
    or make your result window smaller.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidargumentexception
    """

    def __init__(self, message="Invalid argument in the query", original_errors=None):
        super().__init__(message, original_errors)


class InvalidBoardIdError(MondayQueryError):
    """
    Raised when an invalid board ID is provided (HTTP 200).
    This indicates that the board ID being passed in the query is not a valid board ID.
    To resolve, ensure the board ID exists and you have access to the board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidboardidexception
    """

    def __init__(self, message="Invalid board ID", original_errors=None):
        super().__init__(message, original_errors)


class InvalidColumnIdError(MondayQueryError):
    """
    Raised when an invalid column ID is provided (HTTP 200).
    This indicates that the column ID being passed in the query is not a valid column ID.
    To resolve, ensure the column ID exists and you have access to the column.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidcolumnidexception
    """

    def __init__(self, message="Invalid column ID", original_errors=None):
        super().__init__(message, original_errors)


class InvalidUserIdError(MondayQueryError):
    """
    Raised when an invalid user ID is provided (HTTP 200).
    This indicates that the user ID being passed in the query is not a valid user ID.
    To resolve, ensure the user ID exists and this user is assigned to your board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invaliduseridexception
    """

    def __init__(self, message="Invalid user ID", original_errors=None):
        super().__init__(message, original_errors)


class InvalidVersionError(MondayQueryError):
    """
    Raised when an invalid API version is requested (HTTP 200).
    This indicates that the requested API version is invalid.
    To resolve, ensure that your request follows the proper format.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidversionexception
    """

    def __init__(self, message="Invalid API version", original_errors=None):
        super().__init__(message, original_errors)


class ItemNameTooLongError(MondayQueryError):
    """
    Raised when the item name exceeds the character limit (HTTP 200).
    This indicates that the item name you have chosen has exceeded the number of characters allowed.
    To resolve, ensure your item name is between 1 and 255 characters long.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemnametoolongexception
    """

    def __init__(self, message="Item name exceeds the allowed character limit", original_errors=None):
        super().__init__(message, original_errors)


class ItemsLimitationError(MondayQueryError):
    """
    Raised when the limit of items on a board is exceeded (HTTP 200).
    This indicates that you have exceeded the limit of items allowed for a board.
    To resolve, keep the number of items on a board below 10,000.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemslimitationexception
    """

    def __init__(self, message="Exceeded the limit of items on the board", original_errors=None):
        super().__init__(message, original_errors)


class JsonParseError(MondayQueryError):
    """
    Raised when there is a JSON parse error (HTTP 400). This indicates an issue interpreting the provided JSON.
    To resolve, verify all JSON is valid using a JSON validator.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#jsonparseexception
    """

    def __init__(self, message="JSON parse error", original_errors=None):
        super().__init__(message, original_errors)


class RecordValidError(MondayQueryError):
    """
    Raised when there is a record validation error (HTTP 422). This indicates that a board has exceeded the number of
    permitted subscribers or a user/team has exceeded the board subscription limit.
    To resolve, optimize board subscribers or reduce board subscriptions.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#recordvalidexception
    """

    def __init__(self, message="Record validation error", original_errors=None):
        super().__init__(message, original_errors)


class ResourceNotFoundError(MondayQueryError):
    """
    Raised when the requested resource is not found (HTTP 200 or 404).
    This indicates that the ID you are attempting to pass in your query is invalid.
    To resolve, ensure the ID of the item, group, or board you’re querying exists.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#resourcenotfoundexception
    """

    def __init__(self, message="Resource not found", original_errors=None):
        super().__init__(message, original_errors)


class UserUnauthorizedError(MondayQueryError):
    """
    Raised when the user does not have the required permissions (HTTP 403).
    This indicates that the user in question does not have permission to perform the action.
    To resolve, check if the user has permission to access or edit the given resource.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#userunauthorizedexception
    """

    def __init__(self, message="User unauthorized", original_errors=None):
        super().__init__(message, original_errors)


class ErrorInfo:
    def __init__(self, response, query):
        self.error_message = response.get('error_message', '')
        self.error_code = response.get('error_code', None)
        self.status_code = response.get('status_code', None)
        self.errors = []
        self.query_by_lines = graphql_parse(query).split("\n")
        self.process_errors(response)
        self.formatted_message = self.format_errors()

    def process_errors(self, response):
        if 'errors' in response:
            for err in response['errors']:
                if isinstance(err, str):
                    self.add_error(err)

                elif isinstance(err, dict):
                    message = err.get('message', '')
                    locations = []
                    if 'locations' in err:
                        for location in err['locations']:
                            line_index = int(location['line'])
                            column_index = int(location['column'])
                            prev_line = f'{line_index - 1}) {self.query_by_lines[line_index - 2]}' \
                                if line_index > 1 and line_index - 2 < len(self.query_by_lines) else ""
                            error_line = f'{line_index}) {self.query_by_lines[line_index - 1]}' if line_index - 1 < len(
                                self.query_by_lines) else ""
                            next_line = f'{line_index + 1}) {self.query_by_lines[line_index]}' if line_index < len(
                                self.query_by_lines) else ""
                            locations.append({
                                'line': line_index,
                                'column': column_index,
                                'prev_line': prev_line,
                                'error_line': error_line,
                                'next_line': next_line
                            })

                    error_code = err['extensions'].get('code', '') if 'extensions' in err else None
                    status_code = err['extensions'].get('status_code', None) if 'extensions' in err else None
                    self.add_error(message, error_code, status_code, locations)

    def add_error(self, message: str, error_code: str = None, status_code: int = None, locations: list = None):
        error_detail = {
            "message": message,
            "locations": locations if locations else [],
            "error_code": error_code,
            "status_code": status_code
        }
        self.errors.append(error_detail)

    def format_errors(self) -> str:
        if not self.errors:
            formatted_message = f"{self.error_message}\n" if self.error_message else "An error occurred\n"
            formatted_message += f"Error Code: {self.error_code}\n" if self.error_code else ""
            formatted_message += f"Status Code: {self.status_code}\n" if self.status_code else ""

        elif len(self.errors) == 1:
            error = self.errors[0]

            if not self.error_message:
                self.error_message = error['message']

            if error['message'] == self.error_message:
                formatted_message = f"{self.error_message}\n" if self.error_message else "An error occurred\n"
                for location in error['locations']:
                    formatted_message += f"Location: Line {location['line']}, Column {location['column']}\n"
                    if location.get('prev_line'):
                        formatted_message += f"       {location['prev_line']}\n"
                    formatted_message += f"       {location['error_line']}\n"
                    if location.get('next_line'):
                        formatted_message += f"       {location['next_line']}\n"
                if not self.error_code:
                    self.error_code = error.get('error_code')
                if not self.status_code:
                    self.status_code = error.get('status_code')

                formatted_message += f"Error Code: {self.error_code}\n" if self.error_code else ""
                formatted_message += f"Status Code: {self.status_code}\n" if self.status_code else ""

            else:
                formatted_message = f"{self.error_message}\n" if self.error_message else "An error occurred\n"

                formatted_message += f"Error Code: {self.error_code}\n" if self.error_code else ""
                formatted_message += f"Status Code: {self.status_code}\n" if self.status_code else ""
                formatted_message += f"\nOther errors: {error['message']}\n"

                for location in error['locations']:
                    formatted_message += f" - Location: Line {location['line']}, Column {location['column']}\n"
                    if location.get('prev_line'):
                        formatted_message += f"       {location['prev_line']}\n"
                    if location.get('error_line'):
                        formatted_message += f"       {location['error_line']}\n"
                    if location.get('next_line'):
                        formatted_message += f"       {location['next_line']}\n"

                formatted_message += f" - Error Code: {error['error_code']}\n" if error.get('error_code') else ''
                formatted_message += f" - Status Code: {error.get('status_code')}\n" if error.get('status_code') else ''
        else:
            if self.error_message:
                formatted_message = f"{self.error_message}\n"

                formatted_message += f"Error Code: {self.error_code}\n" if self.error_code else ""
                formatted_message += f"Status Code: {self.status_code}\n" if self.status_code else ""
                formatted_message += f"\nOther errors:\n"

                for error in self.errors:
                    formatted_message += f"\n{error['message']}\n"
                    for location in error['locations']:
                        formatted_message += f" - Location: Line {location['line']}, Column {location['column']}\n"
                        if location.get('prev_line'):
                            formatted_message += f"       {location['prev_line']}\n"
                        if location.get('error_line'):
                            formatted_message += f"       {location['error_line']}\n"
                        if location.get('next_line'):
                            formatted_message += f"       {location['next_line']}\n"
                    formatted_message += f" - Error Code: {error['error_code']}\n"
                    formatted_message += f" - Status Code: {error['status_code']}\n"
            else:
                formatted_message = "\nMultiple errors occurred:"
                for error in self.errors:
                    formatted_message += f"\n{error['message']}\n"
                    for location in error['locations']:
                        formatted_message += f" - Location: Line {location['line']}, Column {location['column']}\n"
                        if location.get('prev_line'):
                            formatted_message += f"       {location['prev_line']}\n"
                        if location.get('error_line'):
                            formatted_message += f"       {location['error_line']}\n"
                        if location.get('next_line'):
                            formatted_message += f"       {location['next_line']}\n"
                    formatted_message += f" - Error Code: {error['error_code']}\n"
                    formatted_message += f" - Status Code: {error['status_code']}\n"

        return formatted_message
