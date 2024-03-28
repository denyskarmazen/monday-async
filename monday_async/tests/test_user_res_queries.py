from unittest import TestCase
from monday_async.utils.queries import (get_me_query, get_users_query, get_users_by_email_query, get_teams_query,
                                        add_users_to_team_query, remove_users_from_team_query)
from monday_async.utils.types import UserKind
from monday_async.utils.utils import graphql_parse, format_param_value


class UserQueriesTestCase(TestCase):
    def setUp(self):
        self.complexity = "complexity {\n    before\n    query\n    after\n    reset_in_x_seconds\n  }\n"

    def test_get_me_query(self):
        expected_return = f"""
        query {{
            me {{
                id
                name
                title
                location
                phone
                teams {{
                    id 
                    name
                }}
                url
                is_admin
                is_guest
                is_view_only
                is_pending
            }}
        }}
        """
        query = get_me_query()
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_comp = f"""
        query {{
            complexity {{
                before
                query
                after
                reset_in_x_seconds
            }}        
    
            me {{
                id
                name
                title
                location
                phone
                teams {{
                    id 
                    name
                }}
                url
                is_admin
                is_guest
                is_view_only
                is_pending
            }}
        }}
        """
        query_with_comp = get_me_query(with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_comp), graphql_parse(query_with_comp))

    def test_get_users_query(self):
        ids = [123, "321"]
        limit = 50
        kind = UserKind.ALL.value
        newest_first = format_param_value(True)
        page = 4

        expected_return = f"""
        query {{
            users (
                ids: {format_param_value(ids)}, 
                limit: {len(ids)}, 
                kind: all, 
                newest_first: false,
                page: 1
            ) {{
                id
                email
                name
                title
                location
                phone
                teams {{
                    id 
                    name
                }}
                url
                is_admin
                is_guest
                is_view_only
                is_pending
            }}
        }}
        """
        query = get_users_query(user_ids=ids)
        self.assertEqual(graphql_parse(expected_return), query)

        query_with_complexity = get_users_query(user_ids=ids, with_complexity=True)
        self.assertIn(self.complexity, query_with_complexity)

        page_text = f"page: {page}"
        self.assertIn(page_text, get_users_query(page=page), msg="page parameter is not set correctly")

        limit_text = f"limit: {limit}"
        self.assertIn(limit_text, get_users_query(limit=limit), msg="limit parameter is not set correctly")

        kind_text = f"kind: {kind}"
        self.assertIn(kind_text, get_users_query(user_kind=kind), msg="user_kind parameter is not set correctly")

        newest_first_text = f"newest_first: {newest_first}"
        self.assertIn(newest_first_text, get_users_query(newest_first=True),
                      msg="newest_first parameter is not set correctly")

    def test_get_users_by_email_query(self):
        emails = ["user1@example.com", "user2@example.com"]
        kind = UserKind.ALL.value
        newest_first = format_param_value(True)

        expected_return = f"""
                query {{
                    users (
                        emails: {format_param_value(emails)}, 
                        limit: {len(emails)}, 
                        kind: all, 
                        newest_first: false,
                    ) {{
                        id
                        email
                        name
                        title
                        location
                        phone
                        teams {{
                            id 
                            name
                        }}
                        url
                        is_admin
                        is_guest
                        is_view_only
                        is_pending
                    }}
                }}
                """
        query = get_users_by_email_query(user_emails=emails)
        self.assertEqual(graphql_parse(expected_return), query)

        query_with_complexity = get_users_by_email_query(user_emails=emails, with_complexity=True)
        self.assertIn(self.complexity, query_with_complexity)

        kind_text = f"kind: {kind}"
        self.assertIn(kind_text, get_users_by_email_query(user_emails=emails, user_kind=kind),
                      msg="user_kind parameter is not set correctly")

        newest_first_text = f"newest_first: {newest_first}"
        self.assertIn(newest_first_text, get_users_by_email_query(user_emails=emails, newest_first=True),
                      msg="newest_first parameter is not set correctly")

    def test_get_teams_query(self):
        team_ids = ["12345", 54321]

        expected_return = f"""
        query {{
            teams (ids: null) {{
                id
                name
                users {{
                    id
                    email
                    name
                }}
            }}
        }}
        """
        query = get_teams_query()
        self.assertEqual(graphql_parse(expected_return), query)

        query_with_complexity = get_teams_query(with_complexity=True)
        self.assertIn(self.complexity, query_with_complexity, msg="No complexity added")

        with_ids = f"ids: {format_param_value(team_ids)}"
        self.assertIn(with_ids, get_teams_query(team_ids))

    def test_add_users_to_team_query(self):
        team_id = 12345
        user_ids = [12345, "543231"]
        expected_return = f"""
        mutation {{
            add_users_to_team (
                team_id: 12345,
                user_ids: [12345, "543231"]
            ) {{
                successful_users {{
                    name
                    email 
                }}
                failed_users {{
                    name
                    email
                }}
            }}
        }}
        """
        query = add_users_to_team_query(team_id=team_id, user_ids=user_ids)
        self.assertEqual(graphql_parse(expected_return), query)

        query_with_complexity = add_users_to_team_query(team_id=team_id, user_ids=user_ids, with_complexity=True)
        self.assertIn(self.complexity, query_with_complexity)

    def test_remove_users_from_team_query(self):
        team_id = 12345
        user_ids = [12345, "543231"]
        expected_return = f"""
                mutation {{
                    remove_users_from_team (
                        team_id: 12345,
                        user_ids: [12345, "543231"]
                    ) {{
                        successful_users {{
                            name
                            email 
                        }}
                        failed_users {{
                            name
                            email
                        }}
                    }}
                }}
                """
        query = remove_users_from_team_query(team_id=team_id, user_ids=user_ids)
        self.assertEqual(graphql_parse(expected_return), query)

        query_with_complexity = remove_users_from_team_query(team_id=team_id, user_ids=user_ids, with_complexity=True)
        self.assertIn(self.complexity, query_with_complexity)
