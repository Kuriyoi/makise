import logging
from flask import Flask, render_template
from flask_cors import CORS
from src.extensions import db, login_manager
from dotenv import load_dotenv
from os import environ


def initialize_app() -> Flask:
    """Initializes the Flask app.

    This function creates the Flask app instance. It also configures the app instance and registers extensions.

    The app instance is created with the Flask() constructor. The name of the app is passed as an argument. The name
    is used to find resources on the filesystem, and to store the app's instance path. The name is passed as the
    __name__ variable, which is a Python predefined variable, which is set to the name of the module in which it is
    used. In this case, it is set to 'src.app_define'.
    The template_folder and static_folder arguments are passed to the constructor to set the folders where the templates
    and static files are stored, respectively. Those are the html, css, js, etc. files that are used to render the
    frontend.

    The app instance is configured with the config dictionary:
        - SECRET_KEY: keeps the client-side sessions secure.
        - SQLALCHEMY_DATABASE_URI: sets the database URI used for the connection.
        - SQLALCHEMY_TRACK_MODIFICATIONS: if set to True, SQLAlchemy will track modifications of objects and emit
        signals.
        - SQLALCHEMY_ECHO: if set to True, SQLAlchemy will log all the statements issued to stderr which can be useful
        for debugging.

    The register_extensions() function is called to register extensions that need to be initialized with the app
    instance.

    The register_blueprints() function is called to register blueprints. Blueprints are used to organize the app into
    components and separate the app's concerns.

    The register_error_handlers() function is called to register error handlers. Error handlers are used to redirect to
    every error page.

    The CORS() constructor is called to enable CORS. Needed to allow the frontend to make requests to the backend.
    The supports_credentials argument is set to True to allow cookies to be sent with the request.

    Some variables are set to be used in the templates. The jinja_env.globals dictionary is used to set global variables
    that can be accessed from the templates.

    Returns:
        app: The Flask app instance.
    """
    load_dotenv()
    user = environ.get('POSTGRES_USER')
    password = environ.get('POSTGRES_PASSWORD')
    host = environ.get('POSTGRES_HOST')
    port = environ.get('POSTGRES_PORT')
    db_name = environ.get('POSTGRES_DB')

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = 'b3f1e40a708d41d8ba90952864a59b6a'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = False

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    CORS(app, supports_credentials=True)

    app.jinja_env.globals['SELF_LINK'] = '/'
    app.jinja_env.globals['IMG_FOLDER'] = '../static/img'
    app.jinja_env.globals['COVERS_FOLDER'] = '../static/img/covers'
    app.jinja_env.globals['ERRORS_FOLDER'] = '../static/img/errors'
    app.jinja_env.globals['SOCIAL_MEDIA_FOLDER'] = '../static/img/social_media'
    app.jinja_env.globals['CSS_FOLDER'] = '../static/css'
    app.jinja_env.globals['CSS_IMPORT_FOLDER'] = '../static/css/import'
    app.jinja_env.globals['JS_FOLDER'] = '../static/js'
    app.jinja_env.globals['JS_IMPORT_FOLDER'] = '../static/js/import'

    return app


def register_extensions(app: Flask) -> None:
    """Register extensions.

    Extensions need to be initialized with the app instance here. Extensions registered are db and login_manager.

    db is the SQLAlchemy object, which is the ORM used to interact with the database. It needs to be initialized with
    the app instance. This is done by calling init_app() on the db object.
    It is initialized here to avoid circular imports and to allow the db object to be used in other modules.

    login_manager is the Flask-Login object, which is used to manage user sessions. It needs to be initialized with the
    app instance, as the db extension. This is done by calling init_app() on the login_manager object.

    DB models are needed to initialize the databases with the db.create_all() function. This function is called in the
    'with' block to ensure that the app context is active and only when there are any changes to the models.
    If there are no users in the database, the initial data is added to the database.

    Args:
        app (Flask): Flask app

    Returns:
        None
    """
    from src.database.models import User, Address, Manga, Wishlist, Supplier, Review, Payment, Order, OrderManga, New
    from initial_data import add_initial_data

    db.init_app(app)
    with app.app_context():
        db.create_all()
        user = db.session.query(User).first()
    if not user:
        initial_data = add_initial_data()
        with app.app_context():
            for data in initial_data:
                db.session.add_all(data)
                db.session.commit()

    login_manager.init_app(app)
    login_manager.login_view = 'view.sign_in'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return None


def register_blueprints(app: Flask) -> None:
    """Register blueprints.

    Blueprints are used to organize the code into modules and components. They are registered here to avoid circular
    imports.

    The controller blueprint is used in the api, as the 'controller' in Model–view–controller (MVC) pattern.
    The url_prefix argument is set to '/api' to prefix all the routes defined in this blueprint with '/api'.

    The auth blueprint is used in the authorization api. It is used to handle user authentication and registration.

    The view blueprint is used in the view api. It is used to render the frontend.
    The template_folder argument is set to 'templates' to set the folder where the templates are stored.

    Args:
        app (Flask): Flask app

    Returns:
        None
    """
    from src.api.controller import controller
    from src.api.auth import auth
    from src.api.views import view

    app.register_blueprint(controller, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(view, url_prefix='/', template_folder='templates')

    return None


def register_error_handlers(app: Flask) -> None:
    """Register error handlers to redirect to every error page.

    Args:
        app (Flask): Flask app
    """
    @app.errorhandler(400)
    def error_400_handler(error: Exception) -> (str, int):
        """Error 400 handler.

        Args:
            error (Exception): Exception

        Returns:
            (str, int): Error page and error code
        """
        logging.error(error)
        return render_template(
            'error.html', error=error, error_code=400, error_message="""
                La solicitud no ha podido ser procesada debido a datos incorrectos o con un formato incorrecto.
                Verifica tu solicitud y vuelve a intentarlo."""
        ), 400

    @app.errorhandler(401)
    def error_401_handler(error: Exception) -> (str, int):
        """Error 401 handler.

        Args:
            error (Exception): Exception

        Returns:
            (str, int): Error page and error code
        """
        logging.error(error)
        return render_template(
            'error.html', error=error, error_code=401, error_message="""
            Lo sentimos, no tienes autorización para acceder a esta página.
            Asegúrate de haber iniciado sesión correctamente y de tener los permisos necesarios."""
        ), 401

    @app.errorhandler(403)
    def error_403_handler(error: Exception) -> (str, int):
        """Error 403 handler.

        Args:
            error (Exception): Exception

        Returns:
            (str, int): Error page and error code
        """
        logging.error(error)
        return render_template(
            'error.html', error=error, error_code=403, error_message="""
            Lo sentimos, no tienes permisos para acceder a esta página.
            Si crees que esto es un error, contacta con el administrador del sistema."""
        ), 403

    @app.errorhandler(404)
    def error_404_handler(error: Exception) -> (str, int):
        """Error 404 handler.

        Args:
            error (Exception): Exception

        Returns:
            (str, int): Error page and error code
        """
        logging.error(error)
        return render_template(
            'error.html', error=error, error_code=404, error_message="""
            Lo sentimos, la página que estás buscando no ha podido ser encontrada.
            Puede ser que la URL sea incorrecta o que la página haya sido eliminada."""
        ), 404

    @app.errorhandler(500)
    def error_500_handler(error: Exception) -> (str, int):
        """Error 500 handler.

        Args:
            error (Exception): Exception

        Returns:
            (str, int): Error page and error code
        """
        logging.error(error)
        return render_template(
            'error.html', error=error, error_code=500, error_message="""
            Lo sentimos, ha habido un error en el servidor.
            Por favor, contacta con el administrador del sistema."""
        ), 500
