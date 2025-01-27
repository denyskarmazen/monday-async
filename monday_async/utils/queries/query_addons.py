def add_complexity() -> str:
    """This can be added to any query to return its complexity with it"""
    query = f"""
        complexity {{
            before
            query
            after
            reset_in_x_seconds
        }}
    """
    return query


def add_columns() -> str:
    """This can be added to any boards query to return its columns with it"""
    columns = f"""
    columns {{
        id
        title
        type
        settings_str
    }}
    """
    return columns


def add_groups() -> str:
    """This can be added to any boards query to return its groups with it"""
    groups = f"""
    groups {{
        id
        title
        color
        position
    }}
    """
    return groups


def add_column_values() -> str:
    """This can be added to any items query to return its column values with it"""
    column_values = f"""
    column_values {{
        id
        column {{
            title
            settings_str
        }}
        type
        text
        value
        ... on BoardRelationValue {{
            display_value
            linked_item_ids
        }}
        ... on CheckboxValue {{
            checked
        }}
        ... on CountryValue {{
            country {{
                name 
            }}
        }}
        ... on DateValue {{
            date
            time
        }}
        ... on LocationValue {{
            lat
            lng
            address
        }}
        ... on MirrorValue {{
            display_value
            mirrored_items {{
                linked_item {{
                    id
                    name
                }}
            }}
        }}
        ... on PeopleValue {{
            persons_and_teams {{
                id
                kind
            }}
        }}
    }}   
    """
    return column_values


def add_subitems() -> str:
    """This can be added to any items query to return its subitems with it"""
    subitems = f"""
    subitems {{
        id
        name
        url
        state
    }}
    """
    return subitems


def add_updates() -> str:
    """This can be added to any items query to return its updates with it"""
    updates = f"""
    updates (limit: 100) {{
        id
        text_body
        body
        creator_id
        assets {{
            id 
            name
            file_extension
            url
            public_url 
        }}
        replies {{
            id
            text_body
        }}
    }}
    """
    return updates


__all__ = [
    'add_complexity',
    'add_columns',
    'add_groups',
    'add_column_values',
    'add_subitems',
    'add_updates'
]
