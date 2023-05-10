from flask import jsonify, request, Blueprint, flask, redirect, url_for, session, flash, Response
from flask_login import login_required, current_user
from makise_app.extensions import db
from makise_app.database.models import User, Address, Manga, Supplier, Review, Order, OrderManga, New
from makise_app.decorators import admin_required, json_payload, validate_schema
from makise_app.schemas import user_schema
import logging


controller = Blueprint('controller', __name__)


@login_required
@admin_required
@json_payload
@validate_schema(user_schema(required=True))
@controller.route('/user', methods=['POST'])
def create_user() -> (Response, int):
    """Creates a new user.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "email": "example@example.com",
        "password_1": "example1",
        "password_2": "example1",
        "name": "Ex",
        "surname": "Ample",
        "phone_number": "987654321",
        "admin": false
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    email = request.json['email']
    password_1 = request.json['password_1']
    password_2 = request.json['password_2']
    name = request.json['name']
    surname = request.json['surname']
    phone_number = request.json['phone_number']
    admin = request.json['admin']

    user = db.session.query(User).filter_by(email=email).first()

    if user:
        flash('El correo ya está en uso.', category='error')

        return jsonify({'error': 'Email already in use.'}), 400
    else:
        if password_1 != password_2:
            flash('Las contraseñas no coinciden.', category='error')

            return jsonify({'error': "Passwords don't match."}), 400
        else:
            new_user = User(email=email, password=password_1, name=name, surname=surname, phone_number=phone_number,
                            admin=admin)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Usuario creado correctamente.', category='success')

                return jsonify({'user': new_user.get_dict()}), 200
            except Exception as error:
                db.session.rollback()
                flash('Error al crear el usuario.', category='error')
                logging.error(error)

                return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(user_schema(required=False))
@controller.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id: str) -> (Response, int):
    """Updates a user.

    Parameters are passed in the body of the request as JSON. The request must have the following format (not all fields
    are required):
    {
        "email": "example@example.com",
        "password_1": "example1",
        "password_2": "example1",
        "name": "Ex",
        "surname": "Ample",
        "phone_number": "987654321",
        "admin": false
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    if 'email' in parameters:
        user = User.query.filter_by(email=parameters['email']).first()
        if user:
            flash('El correo ya está en uso.', category='error')

            return jsonify({'error': 'Email already in use.'}), 400

    if 'password_1' in parameters and 'password_2' in parameters:
        if parameters['password_1'] != parameters['password_2']:
            flash('Las contraseñas no coinciden.', category='error')

            return jsonify({'error': "Passwords don't match."}), 400

    try:
        user_to_modify = db.session.query(User).filter_by(id=user_id).first()
        if user_to_modify:
            user_to_modify.update(parameters)
            db.session.commit()
            flash('Usuario actualizado correctamente.', category='success')

            return jsonify({'user': user_to_modify.get_dict()}), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@validate_schema(user_schema(required=False))
@controller.route('/user/me', methods=['PUT'])
def update_me() -> (Response, int):
    """Updates the current user.

    Parameters are passed in the body of the request as JSON. The request must have the following format (not all fields
    are required):
    {
        "email": "example@example.com",
        "password_1": "example1",
        "password_2": "example1",
        "name": "Ex",
        "surname": "Ample",
        "phone_number": "987654321",
    }

    As the schema allows for the admin field, it is removed from the parameters before updating the user if it is
    present in the request.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    if 'email' in parameters:
        user = User.query.filter_by(email=parameters['email']).first()
        if user:
            flash('El correo ya está en uso.', category='error')

            return jsonify({'error': 'Email already in use.'}), 400

    if 'password_1' in parameters and 'password_2' in parameters:
        if parameters['password_1'] != parameters['password_2']:
            flash('Las contraseñas no coinciden.', category='error')

            return jsonify({'error': "Passwords don't match."}), 400

    if 'admin' in parameters:
        parameters.pop('admin')

    try:
        user_to_modify = db.session.query(User).filter_by(id=current_user.id).first()
        if user_to_modify:
            user_to_modify.update(parameters)
            db.session.commit()
            flash('Usuario actualizado correctamente.', category='success')

            return jsonify({'user': user_to_modify.get_dict()}), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id: str) -> (Response, int):
    """Deletes a user.

    A user is deleted from the database. The user id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user_to_delete = db.session.query(User).filter_by(id=user_id).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Usuario eliminado correctamente.', category='success')

            return jsonify({'user': user_to_delete.get_dict()}), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/user/<user_id>', methods=['GET'])
def get_user(user_id: str) -> (Response, int):
    """Gets a user.

    A user is retrieved from the database. The user id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            return jsonify({'user': user.get_dict()}), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/user/me', methods=['GET'])
def get_me() -> (Response, int):
    """Gets the logged user.

    The logged user is retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user = db.session.query(User).filter_by(id=current_user.id).first()

        return jsonify({'user': user.get_dict()}), 200
    except Exception as error:
        flash('Error al obtener el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/user', methods=['GET'])
def get_users() -> (Response, int):
    """Gets all users.

    All users are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        users = db.session.query(User).order_by(User.email.asc()).all()

        return jsonify({'users': [user.get_dict() for user in users]}), 200
    except Exception as error:
        flash('Error al obtener los usuarios.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400
