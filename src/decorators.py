import logging
from functools import wraps
from flask import request, jsonify
from flask_login import current_user
from jsonschema import Draft202012Validator as Validator
from werkzeug.exceptions import abort
from jsonschema.exceptions import ValidationError, best_match


def admin_required(function) -> object:
    """Function decorator to check if a user is admin.

    Raises:
        403: If the user is not admin.
    """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin() is False:
            abort(403)
        return function(*args, **kwargs)

    return decorated_function


def json_payload(function) -> object:
    """Function decorator to check if the requested payload is a valid json."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            if request.json:
                return function(*args, **kwargs)
        except Exception:
            return jsonify({"message": "payload must be a valid json"}), 400
    return decorated_function


def validate_schema(schema: dict):
    """Function decorator to validate a json payload against a schema previously defined.

    Args:
        schema (dict): The schema to validate the json payload against.

    Raises:
        ValidationError: If the json payload is not valid against the schema.
    """
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            validator: Validator = Validator(schema)
            try:
                validator.validate(request.json)
            except ValidationError:
                error = best_match(validator.iter_errors(request.json)).message
                logging.error(error)
                return jsonify(error), 400
            return function(*args, **kwargs)
        return decorated_function
    return decorator
