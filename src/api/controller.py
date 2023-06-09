from flask import jsonify, request, Blueprint, flash, Response, session, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from src.extensions import db
from src.database.models import User, Address, Manga, Supplier, Review, Order, OrderManga, New
from src.decorators import admin_required, json_payload, validate_schema
from src.schemas import user_schema, address_schema, manga_schema, supplier_schema, review_schema, new_schema
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


@login_required
@json_payload
@validate_schema(review_schema(required=True))
@controller.route('/review', methods=['POST'])
def create_review() -> (Response, int):
    """Creates a review.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "manga": "b3eda188a3c546f387cea70e940d0e1e",
        "user": "387cea70e940d0e1eb3eda188a3c546f",
        "rating": "4.6",
        "comment": "Me encanta este manga."
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        review = Review(**parameters)
        db.session.add(review)
        db.session.commit()
        flash('Reseña creada correctamente.', category='success')

        return jsonify({'review': review.get_dict()}), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@json_payload
@validate_schema(review_schema(required=False))
@controller.route('/review/<review_id>', methods=['PUT'])
def update_review(review_id: str) -> (Response, int):
    """Updates a review.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    optional):
    {
        "rating": 4.6,
        "comment": "Me encanta este manga."
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        review_to_modify = db.session.query(Review).filter_by(id=review_id).first()
        if review_to_modify:
            review_to_modify.update(**parameters)
            db.session.commit()
            flash('Reseña actualizada correctamente.', category='success')

            return jsonify({'review': review_to_modify.get_dict()}), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/review/<review_id>', methods=['DELETE'])
def delete_review(review_id: str) -> (Response, int):
    """Deletes a review.

    A review is deleted from the database. The review id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        review_to_delete = db.session.query(Review).filter_by(id=review_id).first()
        if review_to_delete:
            db.session.delete(review_to_delete)
            db.session.commit()
            flash('Reseña eliminada correctamente.', category='success')

            return jsonify({'review': review_to_delete.get_dict()}), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/review/<review_id>', methods=['GET'])
def get_review(review_id: str) -> (Response, int):
    """Gets a review.

    A review is retrieved from the database. The review id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        review = db.session.query(Review).filter_by(id=review_id).first()
        if review:
            return jsonify({'review': review.get_dict()}), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/review', methods=['GET'])
def get_reviews() -> (Response, int):
    """Gets all reviews.

    All reviews are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        reviews = db.session.query(Review).all()

        return jsonify({'reviews': [review.get_dict() for review in reviews]}), 200
    except Exception as error:
        flash('Error al obtener las reseñas.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(new_schema(required=True))
@controller.route('/new', methods=['POST'])
def create_new() -> (Response, int):
    """Creates a new.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required except image):
    {
        "title": "Nuevo manga",
        "description": "Este es un nuevo manga.",
        "image": "death_note_black_edition.jpg",
        "category": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        new = New(**parameters)
        db.session.add(new)
        db.session.commit()
        flash('Noticia creada correctamente.', category='success')

        return jsonify({'new': new.get_dict()}), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@json_payload
@validate_schema(new_schema(required=False))
@controller.route('/new/<new_id>', methods=['PUT'])
def update_new(new_id: str) -> (Response, int):
    """Updates a new.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    optional):
    {
        "title": "Nuevo manga",
        "description": "Este es un nuevo manga.",
        "image": "death_note_black_edition.jpg",
        "category": "b3eda188a3c546f387cea70e940d0e1e"
    }

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    parameters = request.json

    try:
        new_to_modify = db.session.query(New).filter_by(id=new_id).first()
        if new_to_modify:
            new_to_modify.update(**parameters)
            db.session.commit()
            flash('Noticia actualizada correctamente.', category='success')

            return jsonify({'new': new_to_modify.get_dict()}), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@admin_required
@controller.route('/new/<new_id>', methods=['DELETE'])
def delete_new(new_id: str) -> (Response, int):
    """Deletes a new.

    A new is deleted from the database. The new id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        new_to_delete = db.session.query(New).filter_by(id=new_id).first()
        if new_to_delete:
            db.session.delete(new_to_delete)
            db.session.commit()
            flash('Noticia eliminada correctamente.', category='success')

            return jsonify({'new': new_to_delete.get_dict()}), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/new/<new_id>', methods=['GET'])
def get_new(new_id: str) -> (Response, int):
    """Gets a new.

    A new is retrieved from the database. The new id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        new = db.session.query(New).filter_by(id=new_id).first()
        if new:
            return jsonify({'new': new.get_dict()}), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/new', methods=['GET'])
def get_news() -> (Response, int):
    """Gets all news.

    All news are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        news = db.session.query(New).all()

        return jsonify({'news': [new.get_dict() for new in news]}), 200
    except Exception as error:
        flash('Error al obtener las noticias.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/order/<order_id>', methods=['GET'])
def get_order(order_id: str) -> (Response, int):
    """Gets an order.

    An order is retrieved from the database. The order id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        order = db.session.query(Order).filter_by(id=order_id).first()
        if order:
            return jsonify({'order': order.get_dict()}), 200
        else:
            flash('El pedido no existe.', category='error')

            return jsonify({'error': 'Order does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el pedido.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@login_required
@controller.route('/order', methods=['GET'])
def get_orders() -> (Response, int):
    """Gets all orders.

    All orders are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        orders = db.session.query(Order).all()

        return jsonify({'orders': [order.get_dict() for order in orders]}), 200
    except Exception as error:
        flash('Error al obtener los pedidos.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


# TODO: ALPHA VERSION SHOPPING CART. TESTING NEEDED. NOT WORKING. USES FUNCTIONS FROM THE OLD MAKISE PROJECT.
@login_required
@controller.route('/cart/add', methods=['POST'])
def add_product_to_cart():
    """Add product to cart. Adds the product with the given id to the cart."""
    quantity = int(request.form['quantity'])
    isbn_manga = request.form['isbn_manga']
    # validate the received values
    if quantity and isbn_manga and request.method == 'POST':
        manga = Manga.query.filter_by(isbn_manga=isbn_manga).one()
        manga_formatted = format_manga(manga)

        item_array = {
            manga_formatted['isbn_manga']:
                {
                    'isbn_manga': manga_formatted['isbn_manga'],
                    'title': manga_formatted['title'],
                    'author': manga_formatted['author'],
                    'description': manga_formatted['description'],
                    'image': manga_formatted['image'],
                    'price': manga_formatted['price'],
                    'stock': manga_formatted['stock'],
                    'demography': manga_formatted['demography'],
                    'publisher': manga_formatted['publisher'],
                    'supplier': manga_formatted['supplier'],
                    'quantity': quantity,
                    'total_price': quantity * manga_formatted['price']
                }
        }

        all_total_price = 0
        all_total_quantity = 0

        session.modified = True
        if 'cart_item' in session:
            if manga_formatted['isbn_manga'] in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if manga_formatted['isbn_manga'] == key:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * manga_formatted['price']
            else:
                session['cart_item'] = array_merge(session['cart_item'], item_array)

            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = item_array
            all_total_quantity = all_total_quantity + quantity
            all_total_price = all_total_price + quantity * manga_formatted['price']

        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

        return redirect(url_for('products'))
    else:
        flash('Error al añadir el producto al carrito.', category='error')
        return jsonify({"error": "Error adding the product to the cart"}), 401


@login_required
@controller.route('/cart/empty')
def empty_cart():
    """Empty cart. Empties the cart."""
    try:
        session.pop('cart_item')
        session.pop('all_total_quantity')
        session.pop('all_total_price')
        flash('Carrito vaciado correctamente.', category='success')

        return redirect(url_for('.products'))
    except Exception as error:
        print(error)
        flash('Error al vaciar el carrito.', category='error')

        return jsonify({"error": f"Error emptying the cart: {error}"}), 401


@login_required
@controller.route('/cart/delete/<isbn_manga>')
def delete_product_from_cart(isbn_manga):
    """Delete product. Deletes the product with the given id from the cart."""
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == isbn_manga:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        flash('Producto eliminado correctamente.', category='success')

        return redirect(url_for('.products'))
    except Exception as error:
        print(error)
        flash('Error al eliminar el producto.', category='error')

        return jsonify({"error": f"Error deleting the product: {error}"}), 401
