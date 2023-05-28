import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
from src.extensions import db
from src.database.models import User
from src.decorators import json_payload, validate_schema
from src.schemas import user_schema, login_schema


auth = Blueprint('auth', __name__)


@json_payload
@validate_schema(login_schema())
@auth.route('/login', methods=['POST'])
def login() -> str | Response:
    """Login user.

    Saves the user in the session and redirects to the home page.

    If the user is not found or the password is incorrect, an error message is flashed.
    If the user is found and the password is correct, the user is logged in and redirected to the home page.

    Returns:
        str | Response: Flask response.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter_by(email=email).first()

    if user:
        if user.check_password(password):
            flash('Sesión iniciada', category='success')
            login_user(user, remember=True)

            return redirect(url_for('views.home'))
        else:
            flash('El correo o la contraseña son incorrectos.', category='error')
    else:
        flash('El correo o la contraseña son incorrectos.', category='error')

    return render_template("login.html", user=current_user)


@login_required
@auth.route('/logout')
def logout() -> Response:
    """Logout user.

    Removes the user from the session and redirects to the login page.

    Returns:
        Response: Flask response.
    """
    logout_user()

    return redirect(url_for('auth.login'))


@json_payload
@validate_schema(user_schema(required=True))
@auth.route('/sign_up', methods=['POST'])
def sign_up() -> str | Response:
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
    email = request.json['email']
    password_1 = request.json['password_1']
    password_2 = request.json['password_2']
    name = request.json['name']
    surname = request.json['surname']
    phone_number = request.json['phone_number']
    admin = False

    user = db.session.query(User).filter_by(email=email).first()

    if user:
        flash('El correo ya está en uso.', category='error')
    else:
        if password_1 != password_2:
            flash('Las contraseñas no coinciden.', category='error')
        else:
            new_user = User(email=email, password=password_1, name=name, surname=surname, phone_number=phone_number,
                            admin=admin)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Usuario creado correctamente.', category='success')
                login_user(new_user, remember=True)

                return redirect(url_for('views.home'))
            except Exception as error:
                db.session.rollback()
                flash('Error al crear el usuario. Vuelve a intentarlo más tarde.', category='error')
                logging.error(error)

    return render_template("sign_up.html")
