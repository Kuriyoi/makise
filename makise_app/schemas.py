def login_schema() -> dict:
    """Function to define a schema for the login.

    It checks if all necessary fields are present and if they are in the correct format.

    Returns:
        dict: The schema for a login.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "email": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        },
        "required": ["email", "password"]
    }

    return schema


def user_schema(required: bool) -> dict:
    """Function to define a schema for a user.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for a user.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "email": {
                "type": "string",
                "minLength": 5,
                "pattern": "[^@\\s]+@[^@\\s]+\\.[^@\\s]+"
            },
            "password_1": {
                "type": "string",
                "minLength": 8,
                "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
            },
            "password_2": {
                "type": "string",
                "minLength": 8,
                "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
            },
            "name": {
                "type": "string",
                "minLength": 2,
            },
            "surname": {
                "type": "string",
                "minLength": 2,
            },
            "phone_number": {
                "type": "string",
                "minLength": 9,
                "maxLength": 9,
                "pattern": "^[0-9]*$"
            },
            "admin": {
                "type": "boolean"
            }
        },
        "required": ["email", "password", "name", "surname", "phone_number", "admin"]
    }

    if required:
        schema["required"] = ["email", "password", "name", "surname", "phone_number"]

    return schema
