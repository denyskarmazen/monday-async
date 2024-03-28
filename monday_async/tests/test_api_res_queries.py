from unittest import TestCase
from monday_async.utils.queries import get_all_api_versions_query, get_current_api_version_query
from monday_async.utils.utils import graphql_parse


class APIQueriesTestCase(TestCase):
    def test_get_current_api_version_query(self):
        expected_return = """
        query {     
            version {
                kind
                value
            }
        }
        """
        query = get_current_api_version_query()
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_complexity = """
        query {
            complexity {
                before
                query
                after
                reset_in_x_seconds
            }    

            version {
                kind
                value
            }
        }
        """
        query_with_complexity = get_current_api_version_query(with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))


    def test_get_all_api_versions_query(self):
        expected_return = """
        query {    
            versions {
                kind
                value
            }
        }
        """
        query = get_all_api_versions_query()
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_complexity = """
        query {
            complexity {
                before
                query
                after
                reset_in_x_seconds
            }    

            versions {
                kind
                value
            }
        }
        """
        query_with_complexity = get_all_api_versions_query(with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))
