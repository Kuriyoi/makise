import os
from datetime import datetime
from flask import jsonify, request, Blueprint, flash, Response, session, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from src.extensions import db
from src.utils import allowed_file, get_uuid
from src.database.models import User, Address, Manga, Supplier, Review, Order, OrderManga, New, Payment, StatusEnum
from src.decorators import admin_required, json_payload, validate_schema
from src.schemas import user_schema, address_schema, manga_schema, supplier_schema, review_schema, new_schema
import logging


controller = Blueprint('controller', __name__)


@controller.route('/user', methods=['POST'])
@login_required
@admin_required
@json_payload
@validate_schema(user_schema(required=True))
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

        return jsonify({'error': 'Email already in use.'}), 409
    else:
        if parameters['password_1'] != parameters['password_2']:
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

                return jsonify(new_user.get_dict()), 201
            except Exception as error:
                db.session.rollback()
                flash('Error al crear el usuario.', category='error')
                logging.error(error)

                return jsonify({'error': str(error)}), 400


@controller.route('/user/<user_id>', methods=['PUT'])
@login_required
@admin_required
@json_payload
@validate_schema(user_schema(required=False))
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

    if 'password_1' in parameters and 'password_2' in parameters:
        if parameters['password_1'] != parameters['password_2']:
            flash('Las contraseñas no coinciden.', category='error')

            return jsonify({'error': "Passwords don't match."}), 400
        else:
            parameters['password'] = parameters['password_1']
            parameters.pop('password_1')
            parameters.pop('password_2')

    try:
        user_to_modify = db.session.query(User).filter_by(id_user=user_id).first()
        if user_to_modify:
            if 'email' in parameters:
                if parameters['email'] == user_to_modify.email:
                    parameters.pop('email')
                else:
                    user = User.query.filter_by(email=parameters['email']).first()
                    if user:
                        flash('El correo ya está en uso.', category='error')

                        return jsonify({'error': 'Email already in use.'}), 400
            db.session.query(User).filter_by(id_user=user_id).update(parameters)
            db.session.commit()

            return jsonify(user_to_modify.get_dict()), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/user/me', methods=['PUT'])
@login_required
@json_payload
@validate_schema(user_schema(required=False))
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

    user_to_modify = db.session.query(User).filter_by(id_user=current_user.id_user).first()

    if not user_to_modify:
        flash('El usuario no existe.', category='error')

        return jsonify({'error': 'User does not exist.'}), 400

    if 'email' in parameters:
        user = User.query.filter_by(email=parameters['email']).first()
        if user:
            if user.id_user != user_to_modify.id_user:
                flash('El correo ya está en uso.', category='error')

                return jsonify({'error': 'Email already in use.'}), 409

    if 'password_1' in parameters and 'password_2' in parameters:
        if parameters['password_1'] != parameters['password_2']:
            flash('Las contraseñas no coinciden.', category='error')
            return jsonify({'error': "Passwords don't match."}), 400
        elif not user_to_modify.check_password(parameters['current_password']):
            flash('Contraseña actual incorrecta.', category='error')
            return jsonify({'error': "Incorrect current password."}), 400
        elif parameters['password_1'] == parameters['current_password']:
            flash('La nueva contraseña no puede ser igual a la actual.', category='error')
            return jsonify({'error': "New password can't be the same as the current one."}), 400
        else:
            user_to_modify.password = parameters['password_1']
            parameters.pop('password_1')
            parameters.pop('password_2')
            parameters.pop('current_password')

            if not parameters:
                try:
                    db.session.commit()
                    flash('Contraseña actualizada correctamente.', category='success')

                    return jsonify(user_to_modify.get_dict()), 200
                except Exception as error:
                    db.session.rollback()
                    flash('Error al actualizar la contraseña.', category='error')
                    logging.error(error)

                    return jsonify({'error': str(error)}), 400

    if 'admin' in parameters:
        parameters.pop('admin')

    try:
        db.session.query(User).filter_by(id_user=current_user.id_user).update(parameters)
        db.session.commit()

        return jsonify(user_to_modify.get_dict()), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/user/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id: str) -> (Response, int):
    """Deletes a user.

    A user is deleted from the database. The user id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user_to_delete = db.session.query(User).filter_by(id_user=user_id).first()
        if user_to_delete:
            if user_to_delete.payments_user or current_user.id_user == user_to_delete.id_user:
                return jsonify({'error': 'User has payments.'}), 409

            if user_to_delete.addresses_user:
                for address in user_to_delete.addresses_user:
                    db.session.delete(address)
            if user_to_delete.reviews_user:
                for review in user_to_delete.reviews_user:
                    db.session.delete(review)
            if user_to_delete.wishlists_user:
                for wishlist in user_to_delete.wishlists_user:
                    db.session.delete(wishlist)

            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Usuario eliminado correctamente.', category='success')

            return jsonify(user_to_delete.get_dict()), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/user/<user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id: str) -> (Response, int):
    """Gets a user.

    A user is retrieved from the database. The user id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user = db.session.query(User).filter_by(id_user=user_id).first()
        if user:
            return jsonify(user.get_dict()), 200
        else:
            flash('El usuario no existe.', category='error')

            return jsonify({'error': 'User does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/user/me', methods=['GET'])
@login_required
def get_me() -> (Response, int):
    """Gets the logged user.

    The logged user is retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        user = db.session.query(User).filter_by(id_user=current_user.id_user).first()

        return jsonify(user.get_dict()), 200
    except Exception as error:
        flash('Error al obtener el usuario.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/user', methods=['GET'])
@login_required
@admin_required
def get_users() -> (Response, int):
    """Gets all users.

    All users are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        users = db.session.query(User).order_by(User.email.asc()).all()

        return jsonify([user.get_dict() for user in users]), 200
    except Exception as error:
        flash('Error al obtener los usuarios.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/address', methods=['POST'])
@login_required
@json_payload
@validate_schema(address_schema(required=True))
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
        if not current_user.is_admin() or 'user' not in parameters:
            address = Address(**parameters, user=current_user.id_user)
        else:
            address = Address(**parameters)

        user = db.session.query(User).filter_by(id_user=address.user).first()
        user.addresses_user.append(address)

        db.session.add(address)
        db.session.commit()
        flash('Dirección creada correctamente.', category='success')

        return jsonify(address.get_dict()), 201
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/address/<address_id>', methods=['PUT'])
@login_required
@json_payload
@validate_schema(address_schema(required=False))
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
        address_to_modify = db.session.query(Address).filter_by(id_address=address_id).first()

        if address_to_modify:
            if not current_user.is_admin():
                if address_to_modify.user != current_user.id_user:
                    flash('No tienes permiso para modificar esta dirección.', category='error')

                    return jsonify({'error': 'You do not have permission to modify this address.'}), 401

            db.session.query(Address).filter_by(id_address=address_id).update(parameters)
            db.session.commit()
            flash('Dirección actualizada correctamente.', category='success')

            return jsonify(address_to_modify.get_dict()), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/address/<address_id>', methods=['DELETE'])
@login_required
def delete_address(address_id: str) -> (Response, int):
    """Deletes an address.

    An address is deleted from the database. The address id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        address_to_delete = db.session.query(Address).filter_by(id_address=address_id).first()
        if address_to_delete:
            if not current_user.is_admin():
                if address_to_delete.user != current_user.id_user:
                    flash('No tienes permiso para eliminar esta dirección.', category='error')

                    return jsonify({'error': 'You do not have permission to delete this address.'}), 401

            if address_to_delete.orders_address:
                return jsonify({'error': 'Address has orders.'}), 409
            db.session.delete(address_to_delete)
            db.session.commit()
            flash('Dirección eliminada correctamente.', category='success')

            return jsonify(address_to_delete.get_dict()), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/address/<address_id>', methods=['GET'])
@login_required
@admin_required
def get_address(address_id: str) -> (Response, int):
    """Gets an address.

    An address is retrieved from the database. The address id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        address = db.session.query(Address).filter_by(id_address=address_id).first()
        if address:
            return jsonify(address.get_dict()), 200
        else:
            flash('La dirección no existe.', category='error')

            return jsonify({'error': 'Address does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la dirección.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/address', methods=['GET'])
@login_required
@admin_required
def get_addresses() -> (Response, int):
    """Gets all addresses.

    All addresses are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        addresses = db.session.query(Address).order_by(Address.address_name.asc()).all()

        return jsonify([address.get_dict() for address in addresses]), 200
    except Exception as error:
        flash('Error al obtener las direcciones.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/manga', methods=['POST'])
@login_required
@admin_required
def create_manga() -> (Response, int):
    """Creates a manga.

    Parameters are passed in the body of the request as multipart/form-data to allow for the image upload.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    if 'title' not in request.form or 'author' not in request.form or 'description' not in request.form or \
            'price' not in request.form or 'stock' not in request.form or 'image' not in request.files or \
            'genre' not in request.form or 'publisher' not in request.form or 'supplier' not in request.form:
        flash('Faltan campos obligatorios.', category='error')

        return jsonify({'error': 'Missing required fields.'}), 400
    elif not request.form['title'] or not request.form['author'] or not request.form['description'] or \
            not request.form['price'] or not request.form['stock'] or not request.files['image'] or \
            not request.form['genre'] or not request.form['publisher'] or not request.form['supplier']:
        flash('Faltan campos obligatorios.', category='error')

        return jsonify({'error': 'Missing required fields.'}), 400
    elif not allowed_file(request.files['image'].filename):
        flash('Formato de imagen no permitido.', category='error')

        return jsonify({'error': 'Image format not allowed.'}), 409

    cover = request.files['image']

    filename = secure_filename(cover.filename)

    parameters = {
        'title': request.form['title'],
        'author': request.form['author'],
        'description': request.form['description'],
        'price': request.form['price'],
        'stock': request.form['stock'],
        'image': filename,
        'genre': request.form['genre'],
        'publisher': request.form['publisher'],
        'supplier': request.form['supplier'],
        'added_date': datetime.now()
    }

    try:
        cover.save(f'static/img/covers/{filename}')

        manga = Manga(**parameters)
        db.session.add(manga)
        db.session.commit()
        flash('Manga creado correctamente.', category='success')

        added_manga = manga.get_dict()
        added_manga['supplier_name'] = manga.supplier_mangas.name

        return jsonify(added_manga), 201
    except Exception as error:
        os.remove(os.path.join('static/img/covers', filename))
        db.session.rollback()
        flash('Error al crear el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/manga/<manga_id>', methods=['PUT'])
@login_required
@admin_required
def update_manga(manga_id: str) -> (Response, int):
    """Updates a manga.

    Parameters are passed in the body of the request as multipart/form-data to allow for the optional image upload.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    if 'title' not in request.form or 'author' not in request.form or 'description' not in request.form or \
            'stock' not in request.form or 'genre' not in request.form or 'publisher' not in request.form or \
            'supplier' not in request.form:
        flash('Faltan campos obligatorios.', category='error')

        return jsonify({'error': 'Missing required fields.'}), 400
    elif not request.form['title'] or not request.form['author'] or not request.form['description'] or \
            not request.form['stock'] or not request.form['genre'] or not request.form['publisher'] or \
            not request.form['supplier']:
        flash('Faltan campos obligatorios.', category='error')

        return jsonify({'error': 'Missing required fields.'}), 400

    if 'image' in request.files:
        if request.files['image']:
            if not allowed_file(request.files['image'].filename):
                flash('Formato de imagen no permitido.', category='error')

                return jsonify({'error': 'Image format not allowed.'}), 409
            else:
                cover = request.files['image']
        else:
            cover = None
    else:
        cover = None

    parameters = {
        'title': request.form['title'],
        'author': request.form['author'],
        'description': request.form['description'],
        'stock': request.form['stock'],
        'genre': request.form['genre'],
        'publisher': request.form['publisher'],
        'supplier': request.form['supplier']
    }

    try:
        if cover:
            filename = secure_filename(cover.filename)
            parameters['image'] = filename
            cover.save(f'static/img/covers/{filename}')
        manga_to_modify = db.session.query(Manga).filter_by(id_manga=manga_id).first()
        if manga_to_modify:
            db.session.query(Manga).filter_by(id_manga=manga_id).update(parameters)
            db.session.commit()
            flash('Manga actualizado correctamente.', category='success')

            edited_manga = manga_to_modify.get_dict()
            edited_manga['supplier_name'] = manga_to_modify.supplier_mangas.name

            return jsonify(edited_manga), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        if cover:
            filename = secure_filename(cover.filename)
            os.remove(os.path.join('static/img/covers', filename))
        db.session.rollback()
        flash('Error al actualizar el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/manga/<manga_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_manga(manga_id: str) -> (Response, int):
    """Deletes a manga.

    A manga is deleted from the database. The manga id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        manga_to_delete = db.session.query(Manga).filter_by(id_manga=manga_id).first()
        if manga_to_delete:
            db.session.delete(manga_to_delete)
            db.session.commit()
            os.remove(os.path.join('static/img/covers', manga_to_delete.image))
            flash('Manga eliminado correctamente.', category='success')

            return jsonify(manga_to_delete.get_dict()), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/manga/<manga_id>', methods=['GET'])
def get_manga(manga_id: str) -> (Response, int):
    """Gets a manga.

    A manga is retrieved from the database. The manga id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        manga = db.session.query(Manga).filter_by(id_manga=manga_id).first()
        if manga:
            return jsonify(manga.get_dict()), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el manga.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/mangas_admin/<simple>', methods=['GET'])
@controller.route('/mangas', methods=['GET'])
@controller.route('/mangas/<sort_by>', methods=['GET'])
@controller.route('/mangas/<sort_by>/<int:page>', methods=['GET'])
def get_mangas(sort_by=None, page=1, simple='not_simple') -> (Response, int):
    """Gets all mangas.

    All mangas are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        if sort_by:
            if sort_by == 'title_asc':
                mangas = db.session.query(Manga).order_by(Manga.title.asc())
            elif sort_by == 'title_desc':
                mangas = db.session.query(Manga).order_by(Manga.title.desc())
            elif sort_by == 'price_asc':
                mangas = db.session.query(Manga).order_by(Manga.price.asc())
            elif sort_by == 'price_desc':
                mangas = db.session.query(Manga).order_by(Manga.price.desc())
            elif sort_by == 'stock_asc':
                mangas = db.session.query(Manga).order_by(Manga.stock.asc())
            elif sort_by == 'stock_desc':
                mangas = db.session.query(Manga).order_by(Manga.stock.desc())
            else:
                return jsonify({'error': 'Invalid sort parameter.'}), 400
        else:
            mangas = db.session.query(Manga).order_by(Manga.title.asc())

        # Lógica de paginación con Flask-SQLAlchemy
        items_per_page = 9
        paginated_mangas = mangas.paginate(page=page, per_page=items_per_page, error_out=False)
        result_mangas = paginated_mangas.items

        products = []
        for manga in mangas:
            manga_to_add = manga.get_dict()
            if session.get('cart'):
                if manga.id_manga in session['cart']:
                    manga.in_cart = True
                else:
                    manga.in_cart = False
            else:
                manga.in_cart = False
            manga_to_add['in_cart'] = manga.in_cart
            manga_to_add['supplier_name'] = manga.supplier_mangas.name
            products.append(manga_to_add)

        if simple == 'simple' and current_user.is_admin():
            return jsonify(products), 200
        else:
            pagination_data = {
                'total_pages': paginated_mangas.pages,
                'current_page': paginated_mangas.page,
                'has_next': paginated_mangas.has_next,
                'has_prev': paginated_mangas.has_prev
            }

        return jsonify(
            {'products': [manga.get_dict() for manga in result_mangas], 'pagination': pagination_data}
        ), 200
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

        if mangas:
            return jsonify([manga.get_dict() for manga in mangas]), 200
        else:
            flash('No se han encontrado mangas.', category='error')

            return jsonify({'error': 'No mangas found.'}), 404
    except Exception as error:
        flash('Error al obtener los mangas.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/supplier', methods=['POST'])
@login_required
@admin_required
@json_payload
@validate_schema(supplier_schema(required=True))
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

        return jsonify(supplier.get_dict()), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/supplier/<supplier_id>', methods=['PUT'])
@login_required
@admin_required
@json_payload
@validate_schema(supplier_schema(required=False))
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
        supplier_to_modify = db.session.query(Supplier).filter_by(id_supplier=supplier_id).first()
        if supplier_to_modify:
            supplier_to_modify.update(**parameters)
            db.session.commit()
            flash('Proveedor actualizado correctamente.', category='success')

            return jsonify(supplier_to_modify.get_dict()), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/supplier/<supplier_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_supplier(supplier_id: str) -> (Response, int):
    """Deletes a supplier.

    A supplier is deleted from the database. The supplier id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        supplier_to_delete = db.session.query(Supplier).filter_by(id_supplier=supplier_id).first()
        if supplier_to_delete:
            db.session.delete(supplier_to_delete)
            db.session.commit()
            flash('Proveedor eliminado correctamente.', category='success')

            return jsonify(supplier_to_delete.get_dict()), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/supplier/<supplier_id>', methods=['GET'])
@login_required
@admin_required
def get_supplier(supplier_id: str) -> (Response, int):
    """Gets a supplier.

    A supplier is retrieved from the database. The supplier id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        supplier = db.session.query(Supplier).filter_by(id_supplier=supplier_id).first()
        if supplier:
            return jsonify(supplier.get_dict()), 200
        else:
            flash('El proveedor no existe.', category='error')

            return jsonify({'error': 'Supplier does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el proveedor.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/supplier', methods=['GET'])
@login_required
@admin_required
def get_suppliers() -> (Response, int):
    """Gets all suppliers.

    All suppliers are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        suppliers = db.session.query(Supplier).order_by(Supplier.name.asc()).all()

        return jsonify([supplier.get_dict() for supplier in suppliers]), 200
    except Exception as error:
        flash('Error al obtener los proveedores.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/review', methods=['POST'])
@login_required
@json_payload
@validate_schema(review_schema(required=True))
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
        review = Review(**parameters, user=current_user.id_user, date=datetime.now())
        db.session.add(review)
        db.session.commit()
        flash('Reseña creada correctamente.', category='success')

        return jsonify(review.get_dict()), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/review/<manga_id>', methods=['PUT'])
@login_required
@json_payload
@validate_schema(review_schema(required=False))
def update_review(manga_id: str) -> (Response, int):
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
        review_to_modify = db.session.query(Review).filter_by(user=current_user.id_user, manga=manga_id).first()
        if review_to_modify:
            db.session.query(Review).filter_by(user=current_user.id_user, manga=manga_id).update(parameters)
            db.session.commit()
            flash('Reseña actualizada correctamente.', category='success')

            return jsonify(review_to_modify.get_dict()), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/review/<review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id: str) -> (Response, int):
    """Deletes a review.

    A review is deleted from the database. The review id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        review_to_delete = db.session.query(Review).filter_by(id_review=review_id).first()
        if review_to_delete:
            db.session.delete(review_to_delete)
            db.session.commit()
            flash('Reseña eliminada correctamente.', category='success')

            return jsonify(review_to_delete.get_dict()), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/review/<review_id>', methods=['GET'])
@login_required
def get_review(review_id: str) -> (Response, int):
    """Gets a review.

    A review is retrieved from the database. The review id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        review = db.session.query(Review).filter_by(id_review=review_id).first()
        if review:
            return jsonify(review.get_dict()), 200
        else:
            flash('La reseña no existe.', category='error')

            return jsonify({'error': 'Review does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la reseña.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/review', methods=['GET'])
@login_required
def get_reviews() -> (Response, int):
    """Gets all reviews.

    All reviews are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        reviews = db.session.query(Review).all()

        return jsonify([review.get_dict() for review in reviews]), 200
    except Exception as error:
        flash('Error al obtener las reseñas.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/new', methods=['POST'])
@login_required
@admin_required
@json_payload
@validate_schema(new_schema(required=True))
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

        return jsonify(new.get_dict()), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al crear la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/new/<new_id>', methods=['PUT'])
@login_required
@admin_required
@json_payload
@validate_schema(new_schema(required=False))
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
        new_to_modify = db.session.query(New).filter_by(id_new=new_id).first()
        if new_to_modify:
            new_to_modify.update(**parameters)
            db.session.commit()
            flash('Noticia actualizada correctamente.', category='success')

            return jsonify(new_to_modify.get_dict()), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/new/<new_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_new(new_id: str) -> (Response, int):
    """Deletes a new.

    A new is deleted from the database. The new id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        new_to_delete = db.session.query(New).filter_by(id_new=new_id).first()
        if new_to_delete:
            db.session.delete(new_to_delete)
            db.session.commit()
            flash('Noticia eliminada correctamente.', category='success')

            return jsonify(new_to_delete.get_dict()), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al eliminar la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/new/<new_id>', methods=['GET'])
@login_required
def get_new(new_id: str) -> (Response, int):
    """Gets a new.

    A new is retrieved from the database. The new id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        new = db.session.query(New).filter_by(id_new=new_id).first()
        if new:
            return jsonify(new.get_dict()), 200
        else:
            flash('La noticia no existe.', category='error')

            return jsonify({'error': 'New does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener la noticia.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/new', methods=['GET'])
@login_required
def get_news() -> (Response, int):
    """Gets all news.

    All news are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        news = db.session.query(New).all()

        return jsonify([new.get_dict() for new in news]), 200
    except Exception as error:
        flash('Error al obtener las noticias.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/order/<order_id>', methods=['GET'])
@login_required
@admin_required
def get_order(order_id: str) -> (Response, int):
    """Gets an order.

    An order is retrieved from the database. The order id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        order = db.session.query(Order).filter_by(id_order=order_id).first()
        if order:
            return jsonify(order.get_dict()), 200
        else:
            flash('El pedido no existe.', category='error')

            return jsonify({'error': 'Order does not exist.'}), 400
    except Exception as error:
        flash('Error al obtener el pedido.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/order', methods=['GET'])
@login_required
@admin_required
def get_orders() -> (Response, int):
    """Gets all orders.

    All orders are retrieved from the database.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        orders = db.session.query(Order).all()

        return jsonify([order.get_dict() for order in orders]), 200
    except Exception as error:
        flash('Error al obtener los pedidos.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/order', methods=['PUT'])
@login_required
def update_order() -> (Response, int):
    """Updates an order.

    An order is updated in the database. The order id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    order_id = request.json['order_id']
    status = request.json['status']

    try:
        order = db.session.query(Order).filter_by(id_order=order_id).first()
        if order:
            if current_user.is_admin() or order.user_orders.id_user == current_user.id_user:
                order.status = status
                db.session.commit()
                flash('Pedido actualizado correctamente.', category='success')

                return jsonify(order.get_dict()), 200
            else:
                flash('No tienes permiso para actualizar este pedido.', category='error')

                return jsonify({'error': 'You do not have permission to update this order.'}), 401
        else:
            flash('El pedido no existe.', category='error')

            return jsonify({'error': 'Order does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al actualizar el pedido.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/order/cancel/<order_id>', methods=['PUT'])
@login_required
@admin_required
def cancel_order(order_id: str) -> (Response, int):
    """Cancels an order.

    An order is cancelled in the database. The order id is passed as a parameter in the URL.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        order = db.session.query(Order).filter_by(id_order=order_id).first()
        if order:
            db.session.query(Order).filter_by(id_order=order_id).update({'order_status': StatusEnum.cancelled})
            db.session.commit()
            flash('Pedido cancelado correctamente.', category='success')

            return jsonify(order.get_dict()), 200
        else:
            flash('El pedido no existe.', category='error')

            return jsonify({'error': 'Order does not exist.'}), 400
    except Exception as error:
        db.session.rollback()
        flash('Error al cancelar el pedido.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/cart/add', methods=['POST'])
def add_to_cart() -> (Response, int):
    """Adds a manga to the cart.

    A manga is added to the cart. It's done with sessions, so the cart is saved in the server.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    manga_id = request.json['product_id']
    quantity = request.json['quantity']

    try:
        manga = db.session.query(Manga).filter_by(id_manga=manga_id).first()
        if manga:
            if 'cart' not in session:
                session['cart'] = {}
                session['cart_quantity'] = 0

            if manga_id in session['cart']:
                if int(quantity) > manga.stock:
                    flash('No hay suficiente stock.', category='error')

                    return jsonify({'error': 'Not enough stock.', 'stock': manga.stock}), 200

            session['cart'][manga_id] = int(quantity)

            total_price = 0
            cart_quantity = 0

            for manga, quantity in session['cart'].items():
                manga = db.session.query(Manga).filter_by(id_manga=manga).first()
                total_price += manga.price * quantity
                cart_quantity += quantity

            session['total_price'] = total_price
            session['cart_quantity'] = cart_quantity

            session.modified = True

            return jsonify({
                'cart': session['cart'], 'cart_quantity': session['cart_quantity'],
                'total_price': session['total_price']
            }), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        flash('Error al añadir el manga al carrito.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart() -> (Response, int):
    """Removes a manga from the cart.

    A manga is removed from the cart. It's done with sessions, so the cart is saved in the server.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    manga_id = request.json['product_id']

    try:
        manga = db.session.query(Manga).filter_by(id_manga=manga_id).first()
        if manga:
            if 'cart' not in session:
                session['cart'] = {}
                session['cart_quantity'] = 0

            if manga_id in session['cart']:
                del session['cart'][manga_id]

            total_price = 0
            cart_quantity = 0

            for manga, quantity in session['cart'].items():
                manga = db.session.query(Manga).filter_by(id_manga=manga).first()
                total_price += manga.price * quantity
                cart_quantity += quantity

            session['total_price'] = total_price
            session['cart_quantity'] = cart_quantity

            session.modified = True

            if session['cart_quantity'] == 0:
                session['cart'] = {}
                session['cart_quantity'] = 0
                session['total_price'] = 0

                session.modified = True

                return redirect(url_for('view.shopping_cart')), 302

            return jsonify({
                'cart': session['cart'], 'cart_quantity': session['cart_quantity'],
                'total_price': session['total_price']
            }), 200
        else:
            flash('El manga no existe.', category='error')

            return jsonify({'error': 'Manga does not exist.'}), 400
    except Exception as error:
        flash('Error al eliminar el manga del carrito.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/empty_cart', methods=['POST'])
@login_required
def empty_cart() -> (Response, int):
    """Empties the cart.

    The cart is emptied. It's done with sessions, so the cart is saved in the server.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        session['cart'] = {}
        session['cart_quantity'] = 0
        session['total_price'] = 0

        session.modified = True

        return jsonify({'cart': session['cart'], 'cart_quantity': session['cart_quantity']}), 200
    except Exception as error:
        flash('Error al vaciar el carrito.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400


@controller.route('/checkout', methods=['POST'])
@login_required
def checkout() -> (Response, int):
    """Checks out the cart.

    The cart is checked out. It's done with sessions, so the cart is saved in the server.

    Returns:
        Response: Flask response.
        int: HTTP status code.
    """
    try:
        if 'cart' not in session:
            session['cart'] = {}
            session['cart_quantity'] = 0

        if 'address' not in request.json:
            flash('No se ha seleccionado ninguna dirección.', category='error')

            return jsonify({'error': 'No address selected.'}), 400
        else:
            address = db.session.query(Address).filter_by(id_address=request.json['address']).first()
            if not address:
                flash('La dirección no existe.', category='error')

                return jsonify({'error': 'Address does not exist.'}), 400

        if session['cart_quantity'] == 0:
            flash('El carrito está vacío.', category='error')

            return jsonify({'error': 'Cart is empty.'}), 400

        user = db.session.query(User).filter_by(id_user=current_user.id_user).first()

        payment = Payment(
            id_payment=get_uuid() ,payment_date=datetime.now(), payment_method='credit_card',
            total_price=session['total_price'] + 2.99, user=user.id_user
        )

        db.session.add(payment)

        order = Order(
            id_order=get_uuid(), date=datetime.now(), order_status='pending', total_price=session['total_price'] + 2.99,
            address=address.id_address, payment=payment.id_payment
        )

        db.session.add(order)

        address.orders_address.append(order)
        payment.order_payments.append(order)
        user.payments_user.append(payment)

        orders_mangas = []

        for manga, quantity in session['cart'].items():
            manga = db.session.query(Manga).filter_by(id_manga=manga).first()
            if manga.stock < quantity:
                flash('No hay suficiente stock.', category='error')

                return jsonify({'error': 'Not enough stock.', 'stock': manga.stock}), 200

            manga.stock -= quantity

            order_manga = OrderManga(id_order=order.id_order, id_manga=manga.id_manga, quantity=quantity)
            orders_mangas.append(order_manga)
            manga.orders_mangas_manga.append(order_manga)
            print('Cuarto')
            order.orders_mangas_order.append(order_manga)
            print('Quinto')

        db.session.add_all(orders_mangas)
        db.session.commit()

        session['cart'] = {}
        session['cart_quantity'] = 0
        session['total_price'] = 0

        session.modified = True

        return jsonify({'cart': session['cart'], 'cart_quantity': session['cart_quantity']}), 200
    except Exception as error:
        db.session.rollback()
        flash('Error al realizar el pedido.', category='error')
        logging.error(error)

        return jsonify({'error': str(error)}), 400
