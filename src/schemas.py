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


def sign_up_schema(required: bool) -> dict:
    """Function to define a schema for the sign-up.

    It checks if all necessary fields are present and if they are in the correct format.

    Returns:
        dict: The schema for a sign-up.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "email": {
                "type": "string",
                "minLength": 5,
                # "pattern": "[^@\\s]+@[^@\\s]+\\.[^@\\s]+"
                "pattern": "^[\\w\\.-]+@[a-zA-Z\\d\\.-]+\\.[a-zA-Z]{2,}$"
            },
            "current_password": {
                "type": "string",
                "minLength": 1
            },
            "password_1": {
                "type": "string",
                "minLength": 8,
                # "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
                "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[\\W_])[a-zA-Z\\d\\W_]{8,}$"
            },
            "password_2": {
                "type": "string",
                "minLength": 8,
                "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[\\W_])[a-zA-Z\\d\\W_]{8,}$"
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
            "address_name": {
                "type": "string",
                "minLength": 1
            },
            "address_line": {
                "type": "string",
                "minLength": 3
            },
            "town": {
                "type": "string",
                "minLength": 1
            },
            "city": {
                "type": "string",
                "minLength": 1
            },
            "zip_code": {
                "type": "string",
                "minLength": 5,
                "maxLength": 5,
                "pattern": "^[0-9]{5}$"
            },
            "user": {
                "type": "string",
                "minLength": 1
            }
        },
        "required": [
            "email", "password_1", "password_2", "name", "surname", "phone_number", "address_name", "address_line",
            "town", "city", "zip_code"
        ]
    }

    if not required:
        schema["required"] = []

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
                # "pattern": "[^@\\s]+@[^@\\s]+\\.[^@\\s]+"
                "pattern": "^[\\w\\.-]+@[a-zA-Z\\d\\.-]+\\.[a-zA-Z]{2,}$"
            },
            "current_password": {
                "type": "string",
                "minLength": 1
            },
            "password_1": {
                "type": "string",
                "minLength": 8,
                # "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
                "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[\\W_])[a-zA-Z\\d\\W_]{8,}$"
            },
            "password_2": {
                "type": "string",
                "minLength": 8,
                "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[\\W_])[a-zA-Z\\d\\W_]{8,}$"
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
        "required": ["email", "password_1", "password_2", "name", "surname", "phone_number"]
    }

    if not required:
        schema["required"] = []

    return schema


def address_schema(required: bool) -> dict:
    """Function to define a schema for an address.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for an address.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "address_name": {
                "type": "string",
                "minLength": 1
            },
            "address_line": {
                "type": "string",
                "minLength": 3
            },
            "town": {
                "type": "string",
                "minLength": 1
            },
            "city": {
                "type": "string",
                "minLength": 1
            },
            "zip_code": {
                "type": "string",
                "minLength": 5,
                "maxLength": 5,
                "pattern": "^[0-9]{5}$"
            },
            "user": {
                "type": "string",
                "minLength": 1
            }
        },
        "required": ["address_name", "address_line", "town", "city", "zip_code"]
    }

    if not required:
        schema["required"] = []

    return schema


def manga_schema(required: bool) -> dict:
    """Function to define a schema for a manga.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for a manga.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "title": {
                "type": "string",
                "minLength": 1,
            },
            "author": {
                "type": "string",
                "minLength": 1,
            },
            "description": {
                "type": "string",
                "minLength": 1,
            },
            "price": {
                "type": "number",
                "minimum": 0
            },
            "stock": {
                "type": "integer",
                "minimum": 0
            },
            "image": {
                "type": "string",
                "minLength": 1,
            },
            "genre": {
                "type": "string",
                "minLength": 1,
            },
            "publisher": {
                "type": "string",
                "minLength": 1,
            },
            "added_date": {
                "type": "date"
            },
            "supplier": {
                "type": "string",
                "minLength": 1,
            }
        },
        "required": ["title", "author", "description", "price", "stock", "image", "category"]
    }

    if not required:
        schema["required"] = []

    return schema


def supplier_schema(required: bool) -> dict:
    """Function to define a schema for a supplier.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for a supplier.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1,
            },
            "email": {
                "type": "string",
                "minLength": 5,
                # "pattern": "[^@\\s]+@[^@\\s]+\\.[^@\\s]+"
                "pattern": "^[\\w\\.-]+@[a-zA-Z\\d\\.-]+\\.[a-zA-Z]{2,}$"
            },
            "contact_phone": {
                "type": "string",
                "minLength": 9,
                "maxLength": 9,
                "pattern": "^[0-9]*$"
            }
        },
        "required": ["name", "email", "contact_phone"]
    }

    if not required:
        schema["required"] = []

    return schema


def review_schema(required: bool) -> dict:
    """Function to define a schema for a review.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for a review.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "comment": {
                "type": "string",
                "minLength": 1,
            },
            "rating": {
                "type": "number",
                "minimum": 1,
                "maximum": 5
            },
            "manga": {
                "type": "string",
                "minLength": 1,
            }
        },
        "required": ["comment", "rating", "manga"]
    }

    if not required:
        schema["required"] = []

    return schema


def new_schema(required: bool) -> dict:
    """Function to define a schema for a new.

    It checks if all necessary fields are present and if they are in the correct format.

    Args:
        required (bool): True if the fields are required, False otherwise.

    Returns:
        dict: The schema for a new.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": 0,
        "properties": {
            "title": {
                "type": "string",
                "minLength": 1,
            },
            "description": {
                "type": "string",
                "minLength": 1,
            },
            "image": {
                "type": "string",
                "minLength": 1,
            },
            "category": {
                "type": "string",
                "minLength": 1,
            }
        },
        "required": ["title", "description", "category"]
    }

    if not required:
        schema["required"] = []

    return schema
