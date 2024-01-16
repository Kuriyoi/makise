import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from src.extensions import db
from src.database.models import User, Address
from src.decorators import json_payload, validate_schema
from src.schemas import sign_up_schema, login_schema


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
@json_payload
@validate_schema(login_schema())
def login() -> {'str | Response', int}:
    """Login user.

    Saves the user in the session and redirects to the home page.

    If the user is not found or the password is incorrect, an error message is flashed.
    If the user is found and the password is correct, the user is logged in and redirected to the home page.

    Returns:
        str | Response: Flask response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))

    if request.method == 'POST':
        parameters = request.json
        email = parameters['email']
        password = parameters['password']

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            if user.check_password(password):
                login_user(user, remember=True)
                flash('Sesión iniciada correctamente', category='success')

                return redirect(url_for('view.home'))
            else:
                flash('El correo o la contraseña son incorrectos.', category='error')
        else:
            flash('El correo o la contraseña son incorrectos.', category='error')

        return render_template("login.html", user=current_user), 401

    return render_template("login.html", user=current_user), 200


@auth.route('/logout')
@login_required
def logout() -> Response:
    """Logout user.

    Removes the user from the session and redirects to the login page.

    Returns:
        Response: Flask response.
    """
    logout_user()
    if session.get('cart'):
        session.pop('cart')
    if session.get('cart_quantity'):
        session.pop('cart_quantity')

    return redirect(url_for('view.home'))


@auth.route('/sign_up', methods=['GET', 'POST'])
@json_payload
@validate_schema(sign_up_schema(required=True))
def sign_up() -> {'str | Response', int}:
    """Signs up a new user.

    Parameters are passed in the body of the request as JSON. The request must have the following format (all fields are
    required):
    {
        "email": "example@example.com",
        "password_1": "example1",
        "password_2": "example1",
        "name": "Ex",
        "surname": "Ample",
        "phone_number": "987654321"
    }

    As the schema allows for the admin field, it is removed from the parameters before updating the user if it is
    present in the request.

    If the user is created successfully, the user is logged in and redirected to the home page.

    Returns:
        str | Response: Flask response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))

    if request.method == 'POST':
        email = request.json['email']
        password_1 = request.json['password_1']
        password_2 = request.json['password_2']
        name = request.json['name']
        surname = request.json['surname']
        phone_number = request.json['phone_number']
        admin = False

        address_name = request.json["address_name"]
        address_line = request.json["address_line"]
        town = request.json["town"]
        city = request.json["city"]
        zip_code = request.json["zip_code"]

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            flash('El correo ya está en uso.', category='error')
            return jsonify({'message': 'El correo ya está en uso.'}), 409
        else:
            if password_1 != password_2:
                flash('Las contraseñas no coinciden.', category='error')
            else:
                new_user = User(email=email, password=password_1, name=name, surname=surname, phone_number=phone_number,
                                admin=admin)
                new_address = Address(address_name=address_name, address_line=address_line, town=town, city=city,
                                      zip_code=zip_code, user=new_user)
                new_user.addresses_user.append(new_address)
                try:
                    db.session.add_all([new_user, new_address])
                    db.session.commit()
                    flash('Usuario y dirección creados correctamente.', category='success')
                    login_user(new_user, remember=True)

                    return redirect(url_for('view.home'))
                except Exception as error:
                    db.session.rollback()
                    flash(
                        'Error al crear el usuario o la dirección. Vuelve a intentarlo más tarde.',
                        category='error'
                    )
                    logging.error(error)

    return render_template("sign_up.html")
