from functools import wraps
from uuid import uuid4
from flask_login import current_user
from werkzeug.exceptions import abort


def get_uuid() -> str:
    """Returns a random UUID."""
    return uuid4().hex
