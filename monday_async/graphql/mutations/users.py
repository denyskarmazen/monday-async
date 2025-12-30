# monday-async
# Copyright 2025 Denys Karmazeniuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from monday_async.core.helpers import format_param_value, graphql_parse
from monday_async.graphql.addons import add_complexity
from monday_async.types import ID, BaseRoleName, Product
from monday_async.types.args import UserAttributesInput


def update_users_role_mutation(
    user_ids: ID | list[ID], new_role: BaseRoleName | str, with_complexity: bool = False
) -> str:
    """
    Construct a mutation to update a user's role. For more information, visit
    https://developer.monday.com/api-reference/reference/users#update-a-users-role

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
        new_role (Union[BaseRoleName, str]): The user's updated role.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    if isinstance(new_role, BaseRoleName):
        role = new_role.value
    elif isinstance(new_role, str):
        role = new_role
    else:
        raise ValueError("role must be of type BaseRoleName or str")

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_users_role (
            user_ids: {format_param_value(user_ids)}, new_role: {role}
        ) {{
            updated_users {{
                id
                name
                is_admin
                is_guest
                is_view_only
            }}
            errors {{
                message
                code
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def deactivate_users_mutation(user_ids: ID | list[ID], with_complexity: bool = False) -> str:
    """
    Construct a mutation to deactivate users from a monday.com account. For more information, visit
    https://developer.monday.com/api-reference/reference/users#deactivate-users

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to deactivate. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        deactivate_users (user_ids: {format_param_value(user_ids)}) {{
            deactivated_users {{
                id
                name
            }}
            errors {{
                message
                code
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def activate_users_mutation(user_ids: ID | list[ID], with_complexity: bool = False) -> str:
    """
    Construct a mutation to re-activates users in a monday.com account. For more information, visit
    https://developer.monday.com/api-reference/reference/users#activate-users

    Args:
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to activate. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        activate_users (user_ids: {format_param_value(user_ids)}) {{
            activated_users {{
                id
                name
            }}
            errors {{
                message
                code
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def update_users_email_domain_mutation(new_domain: str, user_ids: ID | list[ID], with_complexity: bool = False) -> str:
    """
    Construct a mutation to update a user's email domain. For more information, visit
    https://developer.monday.com/api-reference/reference/users#update-a-users-email-domain
    Args:
        new_domain (str): The updated email domain.
        user_ids (Union[ID, List[ID]]): The unique identifiers of the users to update. The maximum is 200.
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_email_domain (
            input: {{
                new_domain: {format_param_value(new_domain)}, user_ids: {format_param_value(user_ids)}
            }}) {{
            updated_users {{
                id
                name
                email
            }}
            errors {{
                message
                code
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def invite_users_mutation(
    emails: str | list[str],
    product: Product | str,
    user_role: BaseRoleName | str,
    with_complexity: bool = False,
) -> str:
    """
    Construct a mutation to invite users to join a monday.com account.
    They will be in a pending status until the invitation is accepted.
    For more information visit: https://developer.monday.com/api-reference/reference/users#invite-users

    Args:
        emails (Union[str, List[str]]): The emails of the users to invite.
        product (Union[Product, str]): The product to invite the users to.
            Valid values: crm, dev, forms, knowledge, service, whiteboard, workflows, work_management
        user_role (Union[BaseRoleName, str]): The invited user's new role.
            Valid values: ADMIN, GUEST, MEMBER, VIEW_ONLY
        with_complexity (bool): Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed Graph QL mutation.
    """
    # Extract enum values (GraphQL enums are unquoted)
    if isinstance(user_role, BaseRoleName):
        role = user_role.value
    elif isinstance(user_role, str):
        role = user_role
    else:
        raise ValueError("user_role must be of type BaseRoleName or str")

    if isinstance(product, Product):
        product_value = product.value
    elif isinstance(product, str):
        product_value = product
    else:
        raise ValueError("product must be of type Product or str")

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        invite_users (
            emails: {format_param_value(emails)}, product: {product_value}, user_role: {role}
        ) {{
            errors {{
                message
                code
                email
            }}
            invited_users {{
                id
                name
                email
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


def update_multiple_users_mutation(
    user_updates: list[tuple[ID, UserAttributesInput]],
    with_complexity: bool = False,
) -> str:
    """
    Construct a mutation to update multiple users' attributes.
    For more information visit: https://developer.monday.com/api-reference/reference/users#update-multiple-users

    Args:
        user_updates: A list of tuples, each containing a user ID and a UserAttributesInput object
            specifying the attributes to update. Example:
            [(123, UserAttributesInput(name="New Name")), (456, UserAttributesInput(title="Manager"))]
        with_complexity: Returns the complexity of the query with the query if set to True.

    Returns:
        str: The constructed GraphQL mutation.
    """
    # Build the user_updates array for GraphQL
    updates_list = []
    for user_id, attributes in user_updates:
        updates_list.append(f"{{user_id: {format_param_value(user_id)}, user_attribute_updates: {attributes}}}")

    user_updates_str = "[" + ", ".join(updates_list) + "]"

    mutation = f"""
    mutation {{{add_complexity() if with_complexity else ""}
        update_multiple_users (
            user_updates: {user_updates_str}
        ) {{
            updated_users {{
                id
                name
                email
                title
                location
                phone
            }}
            errors {{
                message
                code
                user_id
            }}
        }}
    }}
    """
    return graphql_parse(mutation)


__all__ = [
    "activate_users_mutation",
    "deactivate_users_mutation",
    "invite_users_mutation",
    "update_multiple_users_mutation",
    "update_users_email_domain_mutation",
    "update_users_role_mutation",
]
