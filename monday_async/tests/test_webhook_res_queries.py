from unittest import TestCase
from monday_async.utils.queries import (get_webhooks_by_board_id_query, create_webhook_query, delete_webhook_query)
from monday_async.types import WebhookEventType
from monday_async.utils.utils import monday_json_stringify, graphql_parse


class WebhookQueriesTestCase(TestCase):

    def test_monday_json_stringify(self):
        data = {"columnId": "status"}
        expected_data = r'"{\"columnId\": \"status\"}"'

        self.assertEqual(expected_data, monday_json_stringify(data))

    def test_get_webhooks_by_board_id_query(self):
        board_id = 1111111
        expected_return = f"""
        query {{
            webhooks(board_id: {board_id}){{
                id
                event
                board_id
                config
            }}
        }}
        """
        query = get_webhooks_by_board_id_query(board_id=board_id)
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_complexity = f"""
        query {{
            complexity {{
                before
                query
                after
                reset_in_x_seconds
            }}
                    
            webhooks(board_id: {board_id}){{
                id
                event
                board_id
                config
            }}
        }}
        """
        query_with_complexity = get_webhooks_by_board_id_query(board_id=board_id, with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))

    def test_create_webhook_query(self):
        url = "https://test.com/send_webhook"
        board_id = 1111111
        event_type = WebhookEventType.CREATE_ITEM.value
        confing = {"columnId": "status"}

        expected_return = f"""
        mutation {{
            create_webhook (  
                board_id: {board_id},
                url: "{url}", 
                event: {event_type}, 
                config: null
            ) {{
                id
                board_id
                event
                config
            }}
        }}
        """
        query = create_webhook_query(board_id=board_id, url=url, event=event_type)
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_config = f"""
        mutation {{
            create_webhook (
                board_id: {board_id},
                url: "{url}", 
                event: {event_type}, 
                config: {monday_json_stringify(confing)}
            ) {{
                id
                board_id
                event
                config
            }}
        }}
        """
        query_config = create_webhook_query(board_id=board_id, url=url, event=event_type, config=confing)
        self.assertEqual(graphql_parse(expected_return_config), graphql_parse(query_config))

        expected_return_with_complexity = f"""
        mutation {{
            complexity {{
                before
                query
                after
                reset_in_x_seconds
            }}    

            create_webhook (
                board_id: {board_id},
                url: "{url}", 
                event: {event_type}, 
                config: {monday_json_stringify(confing)}
            ) {{
                id
                board_id
                event
                config
            }}
        }}
        """
        query_with_complexity = create_webhook_query(board_id=board_id, url=url, event=event_type, config=confing,
                                                     with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))

    def test_delete_webhook_query(self):
        webhook_id = 12
        expected_return = f"""
        mutation {{
            delete_webhook (id: 12) {{
                id
                board_id
            }}
        }}
        """
        query = delete_webhook_query(webhook_id=webhook_id)
        self.assertEqual(graphql_parse(expected_return), graphql_parse(query))

        expected_return_with_complexity = f"""
        mutation {{
            complexity {{
                before
                query
                after
                reset_in_x_seconds
            }}    
            
            delete_webhook (id: 12) {{
                id
                board_id
            }}
        }}
        """
        query_with_complexity = delete_webhook_query(webhook_id=webhook_id, with_complexity=True)
        self.assertEqual(graphql_parse(expected_return_with_complexity), graphql_parse(query_with_complexity))

