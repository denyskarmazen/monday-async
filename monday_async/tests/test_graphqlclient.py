import unittest
from monday_async.utils.graphqlclient import AsyncGraphQLClient
from monday_async.exceptions import MondayQueryError


class TestGraphQlClient(unittest.TestCase):
    def setUp(self):
        self.endpoint = "https://api.monday.com/v2"
        self.file_endpoint = "https://api.monday.com/v2/file"
        self.token = "abcd123"
        self.headers = {"API-Version": "2023-10"}
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

        new_headers = {"API-Version": "2024-01"}
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

        expected_message = ("\nArgument 'ids' on Field 'boards' has an invalid value (string). Expected type '[ID!]'.\n"
                            "Location: Line 3, Column 3"
                            "\n2)         query {"
                            "\n3)             boards (ids: string){"
                            "\n4)                 items_page (limit: 500) {\n"
                            r"Stack: Unexpected token '<', \"<!doctypeh\"... is not valid JSON")

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
        expected_message = ('\nSome error happened\n  '
                            '- Status Code: 200\n  '
                            '- Error Code: SomeKindOfException\n  '
                            '- Error Data: {}\n')
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
        expected_message = '\nInternal server error\n  - Status Code: 500\n'
        self.assertEqual(err_info.exception.__str__().strip(), expected_message.strip())
