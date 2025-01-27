from monday_async.utils.utils import graphql_parse
from monday_async.utils.queries.query_addons import add_complexity


def get_complexity_query() -> str:
    """
    Construct a query to get the current complexity points. For more information visit
    https://developer.monday.com/api-reference/reference/complexity
    """
    query = f"""query {{{add_complexity()}}}"""
    return graphql_parse(query)


__all__ = [
    'get_complexity_query'
]
