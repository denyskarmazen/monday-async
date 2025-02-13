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

import re
from typing import Dict, List, Union


class MondayAPIError(Exception):
    """
    Base class for all errors returned by monday.com API.
    """

    def __init__(self, message: str, error_code: str = None, status_code: int = None, error_data: dict = None,
                 extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message)
        self.error_code: str = error_code
        self.status_code: int = status_code
        self.error_data: dict = error_data if error_data is not None else {}
        self.extensions: dict = extensions if extensions is not None else {}
        self.path: dict = path if path is not None else {}
        self.partial_data: Union[Dict, List] = partial_data if partial_data is not None else []


class GraphQLValidationError(MondayAPIError):
    """
    Raised when a GraphQL query is invalid (HTTP 400).
    This indicates that the query you are attempting to send is not valid.
    To resolve, ensure your query is properly formatted and does not contain any syntax errors.
    """

    def __init__(self, message="GraphQL query is invalid", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InternalServerError(MondayAPIError):
    """
    Raised when an internal server error occurs (HTTP 500). This is a general error indicating something went wrong.
    Common causes include invalid arguments or malformatted JSON values.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#internal-server-error
    """

    def __init__(self, message: str = "Internal server error occurred", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class APITemporarilyBlockedError(MondayAPIError):
    """
    Raised when the API is temporarily blocked (HTTP 200).
    This indicates that there is an issue with the API and usage has temporarily been blocked.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#api-temporarily-blocked
    """

    def __init__(self, message: str = "API temporarily blocked", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class DailyLimitExceededError(MondayAPIError):
    """
    Raised when the daily API usage limit is exceeded.
    This indicates that the daily limit of requests has been exceeded.
    To resolve, reduce the number of requests sent in a day.
    For more information, visit https://developer.monday.com/api-reference/docs/rate-limits#daily-call-limit
    """

    def __init__(self, message: str = "Daily limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ConcurrencyLimitExceededError(MondayAPIError):
    """
    Raised when the concurrency limit is exceeded (HTTP 429).
    This indicates that the maximum number of queries allowed at once has been exceeded.
    To resolve, reduce the number of concurrent queries and implement a retry mechanism.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#concurrency-limit-exceeded
    """

    def __init__(self, message: str = "Concurrency limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class DepthLimitExceededError(MondayAPIError):
    """
    Raised when the depth limit is exceeded.
    This indicates that the depth limit for the query has been exceeded.
    To resolve, reduce the depth of your queries.
    """

    def __init__(self, message="Depth limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class FieldLimitExceededError(MondayAPIError):
    """
    Raised when there are too many requests running concurrently.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#field-limit-exceeded
    """

    def __init__(self, message="Field limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class RateLimitExceededError(MondayAPIError):
    """
    Raised when the rate limit is exceeded (HTTP 429).
    This indicates that more than 5,000 requests were made in one minute.
    To resolve, reduce the number of requests sent in one minute.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#rate-limit-exceeded
    """

    def __init__(self, message="Rate limit exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class IpRestrictedError(MondayAPIError):
    """
    Raised when access is restricted due to IP address restrictions (HTTP 401).
    This indicates that an account admin has restricted access from specific IP addresses.
    To resolve, confirm that your IP address is not restricted by your account admin.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#your-ip-is-restricted
    """

    def __init__(self, message="Your IP is restricted", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class UnauthorizedError(MondayAPIError):
    """
    Raised when an unauthorized access attempt is made (HTTP 401).
    This indicates that the necessary permissions are not in place to access the data.
    To resolve, ensure your API key is valid and passed in the “Authorization” header.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#unauthorized
    """

    def __init__(self, message="Unauthorized access", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class BadRequestError(MondayAPIError):
    """
    Raised when the request is malformed or incorrect (HTTP 400).
    This indicates that the structure of the query string was passed incorrectly.
    To resolve, ensure your query string is passed with the “query” key, your request is sent as a POST request with a
    JSON body, and that your query does not contain unterminated strings.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#bad-request
    """

    def __init__(self, message="Bad request", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class MissingRequiredPermissionsError(MondayAPIError):
    """
    Raised when required permissions are missing (HTTP 200).
    his indicates that the API operation has exceeded the OAuth permission scopes granted for the app.
    To resolve, review your app's permission scopes to ensure the correct ones are requested.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#missing-required-permissions
    """

    def __init__(self, message="Missing required permissions", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ParseError(MondayAPIError):
    """
    Raised when there is a parse error in the query (HTTP 200).
    This indicates that some formatting in your query string is incorrect.
    To resolve, ensure your query is a valid string and all parentheses, brackets, and curly brackets are closed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#parse-error-on
    """

    def __init__(self, message="Parse error in the query", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ColumnValueError(MondayAPIError):
    """
    Raised when there is an error with the column value formatting (HTTP 200).
    This indicates that the column value you are attempting to send in your query is of the incorrect formatting.
    To resolve, ensure the value conforms with each column’s data structure.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#columnvalueexception
    """

    def __init__(self, message="Column value formatting error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


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
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        pattern = r"budget remaining (\d+) out of \d+ reset in (\d+) seconds"
        match = re.search(pattern, message)
        if match:
            self.remaining_complexity = int(match.group(1))
            self.reset_in = int(match.group(2))
        else:
            self.remaining_complexity = None
            self.reset_in = None
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class MaxComplexityExceededError(MondayAPIError):
    """
    Raised when a single query exceeds the maximum complexity limit (HTTP 200).
    """

    def __init__(self, message="Max complexity exceeded", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class CorrectedValueError(MondayAPIError):
    """
    Raised when there is an error with the value type (HTTP 200).
    This indicates that the value you are attempting to send in your query is of the wrong type.
    To resolve, ensure the column supports the type of value format being passed.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#correctedvalueexception
    """

    def __init__(self, message="Incorrect value type", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class CreateBoardError(MondayAPIError):
    """
    Raised when there is an error creating a board (HTTP 200). This indicates an issue in your query to create a board.
    To resolve, ensure the template ID is valid or the board ID exists if duplicating a board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#createboardexception
    """

    def __init__(self, message="Error creating board", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


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
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidItemIdError(MondayAPIError):
    """
    Raised when an invalid item ID is provided (HTTP 200).
    This indicates that the item ID being passed in the query is not a valid item ID.
    To resolve, ensure the item ID exists and you have access to the item.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invaliditemidexception
    """

    def __init__(self, message="Invalid item ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidBoardIdError(MondayAPIError):
    """
    Raised when an invalid board ID is provided (HTTP 200).
    This indicates that the board ID being passed in the query is not a valid board ID.
    To resolve, ensure the board ID exists and you have access to the board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidboardidexception
    """

    def __init__(self, message="Invalid board ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidColumnIdError(MondayAPIError):
    """
    Raised when an invalid column ID is provided (HTTP 200).
    This indicates that the column ID being passed in the query is not a valid column ID.
    To resolve, ensure the column ID exists and you have access to the column.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidcolumnidexception
    """

    def __init__(self, message="Invalid column ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidUserIdError(MondayAPIError):
    """
    Raised when an invalid user ID is provided (HTTP 200).
    This indicates that the user ID being passed in the query is not a valid user ID.
    To resolve, ensure the user ID exists and this user is assigned to your board.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invaliduseridexception
    """

    def __init__(self, message="Invalid user ID", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidInputError(MondayAPIError):
    """
    Raised when an invalid input is provided.
    This indicates that the input you are providing is invalid.
    To resolve, ensure the input is in the correct format and follows the API documentation.
    """

    def __init__(self, message="Invalid input provided", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class InvalidVersionError(MondayAPIError):
    """
    Raised when an invalid API version is requested (HTTP 200).
    This indicates that the requested API version is invalid.
    To resolve, ensure that your request follows the proper format.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#invalidversionexception
    """

    def __init__(self, message="Invalid API version", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ItemNameTooLongError(MondayAPIError):
    """
    Raised when the item name exceeds the character limit (HTTP 200).
    This indicates that the item name you have chosen has exceeded the number of characters allowed.
    To resolve, ensure your item name is between 1 and 255 characters long.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemnametoolongexception
    """

    def __init__(self, message="Item name exceeds the allowed character limit",
                 error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ItemsLimitationError(MondayAPIError):
    """
    Raised when the limit of items on a board is exceeded (HTTP 200).
    This indicates that you have exceeded the limit of items allowed for a board.
    To resolve, keep the number of items on a board below 10,000.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#itemslimitationexception
    """

    def __init__(self, message="Exceeded the limit of items on the board",
                 error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class JsonParseError(MondayAPIError):
    """
    Raised when there is a JSON parse error (HTTP 400). This indicates an issue interpreting the provided JSON.
    To resolve, verify all JSON is valid using a JSON validator.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#jsonparseexception
    """

    def __init__(self, message="JSON parse error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class RecordValidError(MondayAPIError):
    """
    Raised when there is a record validation error (HTTP 422). This indicates that a board has exceeded the number of
    permitted subscribers or a user/team has exceeded the board subscription limit.
    To resolve, optimize board subscribers or reduce board subscriptions.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#recordvalidexception
    """

    def __init__(self, message="Record validation error", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class ResourceNotFoundError(MondayAPIError):
    """
    Raised when the requested resource is not found (HTTP 200 or 404).
    This indicates that the ID you are attempting to pass in your query is invalid.
    To resolve, ensure the ID of the item, group, or board you’re querying exists.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#resourcenotfoundexception
    """

    def __init__(self, message="Resource not found", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class UserUnauthorizedError(MondayAPIError):
    """
    Raised when the user does not have the required permissions (HTTP 403).
    This indicates that the user in question does not have permission to perform the action.
    To resolve, check if the user has permission to access or edit the given resource.
    For more information, visit https://developer.monday.com/api-reference/docs/errors#userunauthorizedexception
    """

    def __init__(self, message="User unauthorized", error_code: str = None, status_code: int = None,
                 error_data: dict = None, extensions: dict = None, path: dict = None, partial_data: dict = None):
        super().__init__(message, error_code, status_code, error_data,
                         extensions, path, partial_data)


class MultipleErrors(MondayAPIError):
    """
    Special exception for handling multiple API errors in a single response.
    Contains full collection of parsed errors.
    """

    def __init__(self, message: str, errors: List[MondayAPIError], partial_data: dict = None):
        super().__init__(message=message, partial_data=partial_data)
        self.errors = errors
        self.partial_data = partial_data


__all__ = [
    "MondayAPIError", "APITemporarilyBlockedError", "ColumnValueError", "GraphQLValidationError",
    "InternalServerError", "ConcurrencyLimitExceededError", "FieldLimitExceededError", "RateLimitExceededError",
    "IpRestrictedError", "UnauthorizedError", "BadRequestError", "MissingRequiredPermissionsError", "ParseError",
    "ComplexityError", "MaxComplexityExceededError", "CorrectedValueError", "CreateBoardError", "DeleteLastGroupError",
    "InvalidArgumentError", "InvalidItemIdError", "InvalidBoardIdError", "InvalidColumnIdError", "InvalidUserIdError",
    "InvalidVersionError", "ItemNameTooLongError", "ItemsLimitationError", "JsonParseError", "RecordValidError",
    "ResourceNotFoundError", "UserUnauthorizedError", "DailyLimitExceededError", "MultipleErrors", "InvalidInputError",
    "DepthLimitExceededError"
]
