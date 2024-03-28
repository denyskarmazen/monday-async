from unittest import TestCase
from monday_async.utils.types import TargetType
from monday_async.utils.queries import create_notification_query
from monday_async.utils.utils import graphql_parse


class NotificationQueriesTestCase(TestCase):
    def test_create_notification_query(self):
        user_id = 123456
        target_id = 654321
        text = "Notification text"
        target_type = TargetType.PROJECT.value

        expected_return = f"""
        mutation {{
            create_notification (
                user_id: {user_id}, 
                target_id: {target_id}, 
                text: "{text}", 
                target_type: {target_type}
            ) {{
                text
            }}
        }}
        """
        query = create_notification_query(user_id=user_id, target_id=target_id, text=text, target_type=target_type,
                                          with_complexity=False)
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_complexity = f"""
        mutation {{
            complexity {{
                before
                query
                after
                reset_in_x_seconds
            }}
            
            create_notification (
                user_id: {user_id}, 
                target_id: {target_id}, 
                text: "{text}", 
                target_type: {target_type}
            ) {{
                text
            }}
        }}
        """
        query_with_complexity = create_notification_query(user_id=user_id, target_id=target_id, text=text,
                                                          target_type=target_type, with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))
