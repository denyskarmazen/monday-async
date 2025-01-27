from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import graphql_parse


def get_current_api_version_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get the api version used to make the request. For more information, visit
    https://developer.monday.com/api-reference/reference/version

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        version {{
            display_name
            kind
            value
        }}
    }}
    """
    return graphql_parse(query)


def get_all_api_versions_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get all the monday.com api versions available. For more information, visit
    https://developer.monday.com/api-reference/reference/versions

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        versions {{
            display_name
            kind
            value
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_all_api_versions_query',
    'get_current_api_version_query'
]
