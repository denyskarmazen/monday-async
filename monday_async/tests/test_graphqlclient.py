import unittest
from monday_async.utils.graphqlclient import AsyncGraphQLClient
from monday_async.exceptions import MondayQueryError, RateLimitExceededError, UnauthorizedError, InternalServerError


class TestGraphQlClient(unittest.TestCase):
    def setUp(self):
        self.endpoint = "https://api.monday.com/v2"
        self.file_endpoint = "https://api.monday.com/v2/file"
        self.token = "abcd123"
        self.headers = {"API-Version": "2024-07"}
        self.graph_ql_client = AsyncGraphQLClient(self.endpoint)
        self.file_graph_gl_client = AsyncGraphQLClient(self.file_endpoint)

    def test_token_injection(self):
        self.graph_ql_client.inject_token(self.token)
        self.assertEqual(self.token, self.graph_ql_client.token)

        new_token = "efgh456"
        self.graph_ql_client.inject_token(new_token)
        self.assertEqual(new_token, self.graph_ql_client.token)

    def test_headers_injection(self):
        self.graph_ql_client.inject_headers(self.headers)
        self.assertEqual(self.headers, self.graph_ql_client.headers)

        new_headers = {"API-Version": "2024-10"}
        self.graph_ql_client.inject_headers(new_headers)
        self.assertEqual(new_headers, self.graph_ql_client.headers)

    def test_throw_on_error_no_errors(self):
        query = """query { 
                boards {
                    id
                    name
                }
            }"""
        response = {"data": {"boards": [{"id": "41234", "name": "New Board"}]}}
        self.graph_ql_client._throw_on_error(response, query)

    def test_throw_on_error_errors(self):
        query = f"""
        query {{
            boards (ids: {"string"}){{
                items_page (limit: 500) {{
                    cursor
                    items {{
                        id 
                        name 
                    }}
                }}
            }}
        }}
        """

        response = {
            'errors':
                [
                    {
                        'message': "Argument 'ids' on Field 'boards' has an invalid value (string). "
                                   "Expected type '[ID!]'.",
                        'locations': [{'line': 3, 'column': 3}],
                        'stack': r"Unexpected token '<', \"<!doctypeh\"... is not valid JSON",
                        'path': ['query', 'boards', 'ids'],
                        'extensions': {'code': 'argumentLiteralsIncompatible', 'typeName': 'Field',
                                       'argumentName': 'ids'}
                    }
                ],
            'account_id': 111111111}

        with self.assertRaises(MondayQueryError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        expected_message = ("Argument 'ids' on Field 'boards' has an invalid value (string). Expected "
                            "type '[ID!]'.\n"
                            "Location: Line 3, Column 3\n"
                            "       2)   boards(ids: string) {\n"
                            "       3)     items_page(limit: 500) {\n"
                            "            ^\n"
                            "       4)       cursor\n"
                            "Error Code: argumentLiteralsIncompatible")

        self.assertEqual(err_info.exception.__str__().strip(), expected_message.strip())

    def test_throw_on_error_error_code(self):
        query = f"""
        query {{
            boards (ids: {"string"}){{
                items_page (limit: 500) {{
                    cursor
                    items {{
                        id 
                        name 
                    }}
                }}
            }}
        }}
        """

        response = {"error_code": "SomeKindOfException",
                    "status_code": 200,
                    "error_message": "Some error happened",
                    "error_data": {}}

        with self.assertRaises(MondayQueryError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)
        expected_message = 'Some error happened\nError Code: SomeKindOfException\nStatus Code: 200'
        self.assertEqual(err_info.exception.__str__().strip(), expected_message.strip())

    def test_throw_on_error_error_message(self):
        query = f"""
        query {{
            boards (ids: {"string"}){{
                items_page (limit: 500) {{
                    cursor
                    items {{
                        id 
                        name 
                    }}
                }}
            }}
        }}
        """

        response = {"error_message": "Internal server error",
                    "status_code": 500}

        with self.assertRaises(MondayQueryError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)
        expected_message = '\nInternal server error\nStatus Code: 500\n'
        self.assertEqual(err_info.exception.__str__().strip(), expected_message.strip())

    def test_throw_on_error_multiple_errors_with_error_code(self):
        query = """
        {
            boards (ids: "string") {
                items_page (limit: 500) {
                    cursor
                    items {
                        id 
                        name 
                    }
                }
            }
        }
        """

        response = {
            "errors": [
                {
                    "message": "User unauthorized to perform action",
                    "locations": [
                        {
                            "line": 2,
                            "column": 3
                        }
                    ],
                    "extensions": {
                        "code": "UserUnauthorizedException",
                        "status_code": 403
                    }
                },
                {
                    "message": "Parse error on \")\" (RPAREN) at [59, 15]",
                    "locations": [
                        {
                            "line": 59,
                            "column": 15
                        }
                    ],
                    "extensions": {
                        "code": "ParseError",
                        "status_code": 400
                    }
                }
            ],
            "error_message": "Multiple errors occurred",
            "status_code": 500
        }

        with self.assertRaises(MondayQueryError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        actual_message = str(err_info.exception).strip()

        expected_message = ("Multiple errors occurred:\n"
                            "\nUser unauthorized to perform action\n"
                            "Location: Line 2, Column 3\n"
                            "       1) {\n"
                            "       2)   boards(ids: \"string\") {\n"
                            "            ^\n"
                            "       3)     items_page(limit: 500) {\n"
                            " - Error Code: UserUnauthorizedException\n"
                            " - Status Code: 403\n"
                            "\nParse error on \")\" (RPAREN) at [59, 15]\n"
                            "Location: Line 59, Column 15\n"
                            " - Error Code: ParseError\n"
                            " - Status Code: 400\n")

        self.assertEqual(actual_message, expected_message.strip())


    def test_throw_on_error_multiple_errors(self):
        query = """
        {
            boards (ids: "string") {
                items_page (limit: 500) {
                    cursor
                    items {
                        id 
                        name 
                    }
                }
            }
        }
        """

        response = {
            "errors": [
                {
                    "message": "User unauthorized to perform action",
                    "locations": [
                        {
                            "line": 2,
                            "column": 3
                        }
                    ],
                    "extensions": {
                        "code": "UserUnauthorizedException",
                        "status_code": 403
                    }
                },
                {
                    "message": "Parse error on \")\" (RPAREN) at [59, 15]",
                    "locations": [
                        {
                            "line": 59,
                            "column": 15
                        }
                    ],
                    "extensions": {
                        "code": "ParseError",
                        "status_code": 400
                    }
                }
            ]
        }

        with self.assertRaises(MondayQueryError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        actual_message = str(err_info.exception).strip()

        expected_message = ("Multiple errors occurred:\n"
                            "\n"
                            "User unauthorized to perform action\n"
                            "Location: Line 2, Column 3\n"
                            "       1) {\n"
                            "       2)   boards(ids: \"string\") {\n"
                            "            ^\n"
                            "       3)     items_page(limit: 500) {\n"
                            " - Error Code: UserUnauthorizedException\n"
                            " - Status Code: 403\n"
                            "\nParse error on \")\" (RPAREN) at [59, 15]\n"
                            "Location: Line 59, Column 15\n"
                            " - Error Code: ParseError\n"
                            " - Status Code: 400\n")

        self.assertEqual(actual_message, expected_message.strip())

    def test_throw_on_error_specific_error_codes(self):
        query = """
        query {
            boards (ids: "string") {
                items_page (limit: 500) {
                    cursor
                    items {
                        id 
                        name 
                    }
                }
            }
        }
        """

        response = {
            "error_message": "Internal server error",
            "status_code": 500,
            "error_code": "INTERNAL_SERVER_ERROR"
        }

        with self.assertRaises(InternalServerError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        expected_message = "Internal server error\nError Code: INTERNAL_SERVER_ERROR\nStatus Code: 500\n"
        self.assertEqual(str(err_info.exception).strip(), expected_message.strip())

        response = {
            "error_message": "Unauthorized access",
            "status_code": 401,
            "error_code": "Unauthorized"
        }

        with self.assertRaises(UnauthorizedError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        expected_message = "Unauthorized access\nError Code: Unauthorized\nStatus Code: 401\n"
        self.assertEqual(str(err_info.exception).strip(), expected_message.strip())

        response = {
            "error_message": "Rate limit exceeded",
            "status_code": 429,
            "error_code": "RateLimitExceeded"
        }

        with self.assertRaises(RateLimitExceededError) as err_info:
            self.graph_ql_client._throw_on_error(response, query)

        expected_message = "Rate limit exceeded\nError Code: RateLimitExceeded\nStatus Code: 429\n"
        self.assertEqual(str(err_info.exception).strip(), expected_message.strip())
