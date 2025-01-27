from monday_async.utils.queries.query_addons import add_complexity
from monday_async.utils.utils import graphql_parse


def get_account_query(with_complexity: bool = False) -> str:
    """
    Construct a query to get the account details. For more information, visit
    https://developer.monday.com/api-reference/reference/account

    Args:
        with_complexity (bool): returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed query.
    """
    query = f"""
    query {{{add_complexity() if with_complexity else ""}
        account {{
            id
            name
            slug
            tier
            country_code
            plan {{
                max_users
                tier
                period
                version
            }}
        }}
    }}
    """
    return graphql_parse(query)


__all__ = [
    'get_account_query'
]
