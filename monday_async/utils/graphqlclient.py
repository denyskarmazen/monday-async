import os
import json
import aiohttp
import aiofiles
from monday_async.exceptions import *

TOKEN_HEADER = 'Authorization'


class AsyncGraphQLClient:
    """
    A client for interacting with a monday.com GraphQL API asynchronously.

    This client supports executing queries and mutations, including those requiring file uploads.

    Attributes:
        endpoint (str): The URL of the monday.com API endpoint.
        token (str, optional): The bearer token for authentication. Default is None.
        session (aiohttp.ClientSession, optional): Optional, externally managed aiohttp session. Recommended to use
                                                   the same session for all the requests.
                                                   If not provided, the client will create a new session for each
                                                   request which is not optimal.
        headers (dict): Additional headers to send with each request.
    """

    def __init__(self, endpoint):
        """
         Initializes a new instance of the GraphQLClient.

         Parameters:
             endpoint (str): The URL of the GraphQL endpoint.
         """
        self.endpoint = endpoint
        self.token = None
        self.session = None
        self.headers = {}

    async def execute(self, query, variables=None):
        """
        Executes a GraphQL query or mutation.

        Parameters:
            query (str): The GraphQL query or mutation.
            variables (dict, optional): A dictionary of variables for the query. Default is None.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        return await self._send(query, variables)

    def inject_token(self, token):
        """
        Injects an authentication token to be used for all requests.

        Parameters:
            token (str): The bearer token for authentication.
        """
        self.token = token

    def inject_headers(self, headers):
        """
        Injects additional headers to be used for all requests.

        Parameters:
            headers (dict): A dictionary of headers to add to the request.
        """
        self.headers = headers

    def set_session(self, session: aiohttp.ClientSession):
        """
        Sets an external aiohttp.ClientSession to be used by the client.

        This allows for external management of the session's lifecycle.

        Parameters:
            session (aiohttp.ClientSession): An externally managed aiohttp session.
        """
        self.session = session

    async def close_session(self):
        """
        Closes the aiohttp.ClientSession if it was set externally and is no longer needed.

        Important: This method is intended for use cases where the GraphQLClient is
        responsible for session lifecycle management.
        It should be used with caution, as closing a session that's shared or
        managed externally can lead to unexpected behavior.
        """
        if self.session:
            await self.session.close()
            self.session = None

    async def _send(self, query, variables):
        """
        Sends the GraphQL query or mutation to the server.

        This method constructs the appropriate HTTP request based on the presence of variables
        and/or files and handles the response.

        Parameters:
            query (str): The GraphQL query or mutation.
            variables (dict, optional): A dictionary of variables for the query.

        Returns:
            dict: The JSON response from the GraphQL server.

        Raises:
            MondayQueryError: If the GraphQL server returns errors.
        """
        headers = self.headers.copy()

        if self.token is not None:
            headers[TOKEN_HEADER] = self.token

        if variables is None:
            headers.setdefault('Content-Type', 'application/json')

            payload = json.dumps({'query': query}).encode('utf-8')

        else:
            if 'file' in variables:
                filename = os.path.basename(variables['file'])
                map_data = '{"0": ["variables.file"]}'

                data = aiohttp.FormData()
                data.add_field('query', query)
                data.add_field('map', map_data)

                async with aiofiles.open(variables['file'], 'rb') as file:
                    file_content = await file.read()
                    data.add_field('0', file_content, filename=filename, content_type='application/octet-stream')

                payload = data
            else:
                headers.setdefault('Content-Type', 'application/json')

                payload = json.dumps({'query': query, 'variables': variables}).encode('utf-8')

        if not self.session:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.endpoint, headers=headers, data=payload) as response:
                        response_data = await response.json()
                        self._throw_on_error(response_data, query)
                        return response_data
            except (aiohttp.ClientError, json.JSONDecodeError, MondayQueryError) as e:
                if self.session:
                    await self.close_session()
                raise e
        else:
            async with self.session.post(self.endpoint, headers=headers, data=payload) as response:
                response_data = await response.json()
                self._throw_on_error(response_data, query)
                return response_data

    @staticmethod
    def _throw_on_error(response, query: str):
        """
        Analyzes the response from the GraphQL server and raises an exception if there are errors.

        Parameters:
            response (dict): The JSON response from the server.
            query (str): The GraphQL query or mutation that was sent.

        Raises:
            MondayQueryError: If the GraphQL server returns errors.
        """
        error_codes = {
            'INTERNAL_SERVER_ERROR': InternalServerError,
            'MaxConcurrencyExceeded': ConcurrencyLimitExceededError,
            'RateLimitExceeded': RateLimitExceededError,
            'IpRestricted': IpRestrictedError,
            'Unauthorized': UnauthorizedError,
            'BadRequest': BadRequestError,
            'missingRequiredPermissions': MissingRequiredPermissionsError,
            'ParseError': ParseError,
            'ColumnValueException': ColumnValueError,
            'ComplexityException': ComplexityError,
            'CorrectedValueException': CorrectedValueError,
            'CreateBoardException': CreateBoardError,
            'DeleteLastGroupException': DeleteLastGroupError,
            'InvalidArgumentException': InvalidArgumentError,
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

        if (isinstance(response, dict) and
                ('errors' in response or 'error_message' in response or 'error_code' in response)):
            error_info = ErrorInfo(response, query)
            error_class = error_codes.get(error_info.error_code, MondayQueryError)

            if error_info.errors or error_info.error_message:
                raise error_class(error_info.formatted_message)
