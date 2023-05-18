from flask import jsonify, request, Blueprint, flask, redirect, url_for, session, flash, Response
from flask_login import login_required, current_user
from sqlalchemy import or_
from makise_app.extensions import db
from makise_app.database.models import User, Address, Manga, Supplier, Review, Order, OrderManga, New
from makise_app.decorators import admin_required, json_payload, validate_schema
from makise_app.schemas import user_schema, address_schema, manga_schema, supplier_schema
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
    parameters = request.json

    user = db.session.query(User).filter_by(email=parameters['email']).first()

    if user:
        flash('El correo ya está en uso.', category='error')

        return jsonify({'error': 'Email already in use.'}), 400
    else:
        if parameters['password_1'] != parameters['password_1']:
            flash('Las contraseñas no coinciden.', category='error')

            return jsonify({'error': "Passwords don't match."}), 400
        else:
            parameters['password'] = parameters['password_1']
            parameters.pop('password_1')
            parameters.pop('password_2')

            try:
                new_user = User(**parameters)
                db.session.add(new_user)
                db.session.commit()
                flash('Usuario creado correctamente.', category='success')

                return jsonify({'user': new_user.get_dict()}), 201
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
        else:
            parameters['password'] = parameters['password_1']
            parameters.pop('password_1')
            parameters.pop('password_2')

    try:
        user_to_modify = db.session.query(User).filter_by(id=user_id).first()
        if user_to_modify:
            user_to_modify.update(**parameters)
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
@json_payload
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
        else:
            parameters['password'] = parameters['password_1']
            parameters.pop('password_1')
            parameters.pop('password_2')

    if 'admin' in parameters:
        parameters.pop('admin')

    try:
        user_to_modify = db.session.query(User).filter_by(id=current_user.id).first()
        if user_to_modify:
            user_to_modify.update(**parameters)
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


@login_required
@admin_required
@json_payload
@validate_schema(address_schema(required=True))
@controller.route('/address', methods=['POST'])
def create_address() -> (Response, int):
    """Creates an address.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "address_name": "Example Address",
        "address_line": "Example Street, 1",
        "town": "Townsville",
        "city": "Grand City",
        "zip_code": "12345",
        "country": "Spain",
        "user": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        address = Address(**parameters)
        db.session.add(address)
        db.session.commit()
        flash('Dirección creada correctamente.', category='success')

        return jsonify({'address': address.get_dict()}), 201
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(address_schema(required=False))
@controller.route('/address/<address_id>', methods=['PUT'])
def update_address(address_id: str) -> (Response, int):
    """Updates an address.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    optional):
    {
        "address_name": "Example Address",
        "address_line": "Example Street, 1",
        "town": "Townsville",
        "city": "Grand City",
        "zip_code": "12345",
        "country": "Spain",
        "user": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        address_to_modify = db.session.query(Address).filter_by(id=address_id).first()
        if address_to_modify:
            address_to_modify.update(**parameters)
            db.session.commit()
            flash('Dirección actualizada correctamente.', category='success')

            return jsonify({'address': address_to_modify.get_dict()}), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/address/<address_id>', methods=['DELETE'])
def delete_address(address_id: str) -> (Response, int):
    """Deletes an address.

    An address is deleted from the database. The address id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        address_to_delete = db.session.query(Address).filter_by(id=address_id).first()
        if address_to_delete:
            db.session.delete(address_to_delete)
            db.session.commit()
            flash('Dirección eliminada correctamente.', category='success')

            return jsonify({'address': address_to_delete.get_dict()}), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/address/<address_id>', methods=['GET'])
def get_address(address_id: str) -> (Response, int):
    """Gets an address.

    An address is retrieved from the database. The address id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        address = db.session.query(Address).filter_by(id=address_id).first()
        if address:
            return jsonify({'address': address.get_dict()}), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/address', methods=['GET'])
def get_addresses() -> (Response, int):
    """Gets all addresses.

    All addresses are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        addresses = db.session.query(Address).order_by(Address.address_name.asc()).all()

        return jsonify({'addresses': [address.get_dict() for address in addresses]}), 200
    except Exception as error:
        flash('Error al obtener las direcciones.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(manga_schema(required=True))
@controller.route('/manga', methods=['POST'])
def create_manga() -> (Response, int):
    """Creates a manga.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "title": "Death Note Black Edition
        "author": "Tsugumi Ohba / Takeshi Obata",
        "description": "Light Yagami founds a notebook that can kill people whose name is written on it.",
        "price": 15,
        "stock": 20,
        "image": "death_note_black_edition.jpg",
        "genre": "Shonen",
        "publisher": "Norma Editorial",
        "publication_date": "2012-01-01",
        "supplier": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        manga = Manga(**parameters)
        db.session.add(manga)
        db.session.commit()
        flash('Manga creado correctamente.', category='success')

        return jsonify({'manga': manga.get_dict()}), 201
    except Exception as error:
        db.session.rollback()
        flash('Error al crear el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(manga_schema(required=False))
@controller.route('/manga/<manga_id>', methods=['PUT'])
def update_manga(manga_id: str) -> (Response, int):
    """Updates a manga.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    optional):
    {
        "title": "Death Note Black Edition
        "author": "Tsugumi Ohba / Takeshi Obata",
        "description": "Light Yagami founds a notebook that can kill people whose name is written on it.",
        "price": 15,
        "stock": 20,
        "image": "death_note_black_edition.jpg",
        "genre": "Shonen",
        "publisher": "Norma Editorial",
        "publication_date": "2012-01-01",
        "supplier": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        manga_to_modify = db.session.query(Manga).filter_by(id=manga_id).first()
        if manga_to_modify:
            manga_to_modify.update(**parameters)
            db.session.commit()
            flash('Manga actualizado correctamente.', category='success')

            return jsonify({'manga': manga_to_modify.get_dict()}), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/manga/<manga_id>', methods=['DELETE'])
def delete_manga(manga_id: str) -> (Response, int):
    """Deletes a manga.

    A manga is deleted from the database. The manga id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        manga_to_delete = db.session.query(Manga).filter_by(id=manga_id).first()
        if manga_to_delete:
            db.session.delete(manga_to_delete)
            db.session.commit()
            flash('Manga eliminado correctamente.', category='success')

            return jsonify({'manga': manga_to_delete.get_dict()}), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/manga/<manga_id>', methods=['GET'])
def get_manga(manga_id: str) -> (Response, int):
    """Gets a manga.

    A manga is retrieved from the database. The manga id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        manga = db.session.query(Manga).filter_by(id=manga_id).first()
        if manga:
            return jsonify({'manga': manga.get_dict()}), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/manga', methods=['GET'])
def get_mangas() -> (Response, int):
    """Gets all mangas.

    All mangas are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        mangas = db.session.query(Manga).order_by(Manga.title.asc()).all()

        return jsonify({'mangas': [manga.get_dict() for manga in mangas]}), 200
    except Exception as error:
        flash('Error al obtener los mangas.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/manga/search/<search_term>', methods=['GET'])
def search_mangas(search_term: str) -> (Response, int):
    """Searches for mangas.

    Mangas are retrieved from the database based on the search term passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        mangas = db.session.query(Manga).filter(or_(Manga.title.ilike(f'%{search_term}%'),
                                                    Manga.author.ilike(f'%{search_term}%'),
                                                    Manga.genre.ilike(f'%{search_term}%'),
                                                    Manga.publisher.ilike(f'%{search_term}%'))).all()

        return jsonify({'mangas': [manga.get_dict() for manga in mangas]}), 200
    except Exception as error:
        flash('Error al obtener los mangas.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(supplier_schema(required=True))
@controller.route('/supplier', methods=['POST'])
def create_supplier() -> (Response, int):
    """Creates a supplier.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "name": "SD Distribuciones",
        "contact_phone": "987654321",
        "email": "example@example.com"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        supplier = Supplier(**parameters)
        db.session.add(supplier)
        db.session.commit()
        flash('Proveedor creado correctamente.', category='success')

        return jsonify({'supplier': supplier.get_dict()}), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(supplier_schema(required=False))
@controller.route('/supplier/<supplier_id>', methods=['PUT'])
def update_supplier(supplier_id: str) -> (Response, int):
    """Updates a supplier.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    optional):
    {
        "name": "SD Distribuciones",
        "contact_phone": "987654321",
        "email": "example@example.com"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """

    parameters = request.json

    try:
        supplier_to_modify = db.session.query(Supplier).filter_by(id=supplier_id).first()
        if supplier_to_modify:
            supplier_to_modify.update(**parameters)
            db.session.commit()
            flash('Proveedor actualizado correctamente.', category='success')

            return jsonify({'supplier': supplier_to_modify.get_dict()}), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/supplier/<supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id: str) -> (Response, int):
    """Deletes a supplier.

    A supplier is deleted from the database. The supplier id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        supplier_to_delete = db.session.query(Supplier).filter_by(id=supplier_id).first()
        if supplier_to_delete:
            db.session.delete(supplier_to_delete)
            db.session.commit()
            flash('Proveedor eliminado correctamente.', category='success')

            return jsonify({'supplier': supplier_to_delete.get_dict()}), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/supplier/<supplier_id>', methods=['GET'])
def get_supplier(supplier_id: str) -> (Response, int):
    """Gets a supplier.

    A supplier is retrieved from the database. The supplier id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        supplier = db.session.query(Supplier).filter_by(id=supplier_id).first()
        if supplier:
            return jsonify({'supplier': supplier.get_dict()}), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/supplier', methods=['GET'])
def get_suppliers() -> (Response, int):
    """Gets all suppliers.

    All suppliers are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        suppliers = db.session.query(Supplier).order_by(Supplier.name.asc()).all()

        return jsonify({'suppliers': [supplier.get_dict() for supplier in suppliers]}), 200
    except Exception as error:
        flash('Error al obtener los proveedores.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400
