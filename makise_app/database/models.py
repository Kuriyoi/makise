from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from makise_app.extensions import db
from makise_app.utils import get_uuid
from datetime import datetime


Model = db.Model
Column = db.Column
Integer = db.Integer
Float = db.Float
String = db.String
Text = db.Text
Boolean = db.Boolean
ForeignKey = db.ForeignKey
DateTime = db.DateTime
relationship = db.relationship
Enum = db.Enum


class User(Model, UserMixin):
    """User model.

    Attributes:
        id_user (str): User's id.
        email (str): User's email.
        _password (str): User's password.
        name (str): User's name.
        surname (str): User's surname.
        phone_number (str): User's phone number.
        admin (bool): User's admin status. True if user is admin.
    """
    __tablename__ = "users"

    id_user = Column(String(35), primary_key=get_uuid)
    email = Column(String(100), unique=True, nullable=False)
    _password = Column(Text, nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=False)
    phone_number = Column(String(9), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    address = relationship("Address", backref="user", lazy=True)
    order = relationship("Order", backref="user", lazy=True)
    review = relationship("Review", backref="user", lazy=True)
    new = relationship("New", backref="user", lazy=True)

    @hybrid_property
    def password(self):
        """Password getter, needed because password property is private.

        Returns:
            str: Hashed password.
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Password setter.

        Hashes password and sets it to _password attribute.

        Args:
            value (str): Password to hash.

        Returns:
            None
        """
        self._password = generate_password_hash(value)

    def __init__(self, email: str, password: str, name: str, surname: str, phone_number: str, admin: bool = False):
        """User constructor."""
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.admin = admin

    def __repr__(self) -> str:
        """User representation.

        Returns:
            str: User's email, name and surname.
        """
        return f"{self.email}, {self.name} {self.surname}"

    def check_password(self, password: str) -> bool:
        """Check if a password is correct.

        Args:
            password (str): Password to check.

        Returns:
            bool: True if password is correct.
        """
        return check_password_hash(self._password, password)

    def is_admin(self) -> bool:
        """Check if a user is admin.

        Returns:
            bool: True if user is admin.
        """
        return self.admin

    def get_dict(self) -> dict:
        """Get user's data in a dictionary.

        Returns:
            dict: User's data.
        """
        return {
            "id_user": self.id_user,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "admin": self.admin
        }

    def update_from_api(self):
        """Update user's data from API."""
        pass


class Address(Model):
    """Address model.

    Attributes:
        id_address (str): Address's id.
        address_name (str): Address's name.
        address_line (str): Address's line.
        town (str): Address's town.
        city (str): Address's city.
        zip_code (str): Address's zip code.
        country (str): Address's country.
        user (str): User who owns the address. Foreign key to User model.
    """
    __tablename__ = "addresses"

    id_address = Column(String(35), primary_key=get_uuid)
    address_name = Column(String(20), nullable=False)
    address_line = Column(String(100), nullable=False)
    town = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    zip_code = Column(String(5), nullable=False)
    country = Column(String(50), nullable=False)
    user = Column(String(35), ForeignKey("users.id_user"), nullable=False)
    order = relationship("Order", backref="address", lazy=True)

    def __init__(self, address_name, address_line, town, city, zip_code, country, user):
        """Address constructor."""
        self.address_name = address_name
        self.address_line = address_line
        self.town = town
        self.city = city
        self.zip_code = zip_code
        self.country = country
        self.user = user

    def __repr__(self):
        """Address representation.

        Returns:
            str: Address's line, town, city, zip code and country.
        """
        return f"{self.address_line}, {self.town}, {self.city}, {self.zip_code}, {self.country}"

    def get_dict(self) -> dict:
        """Get address's data in a dictionary.

        Returns:
            dict: Address's data.
        """
        return {
            "id_address": self.id_address,
            "address_name": self.address_name,
            "address_line": self.address_line,
            "town": self.town,
            "city": self.city,
            "zip_code": self.zip_code,
            "country": self.country,
            "user": self.user
        }


class Manga(Model):
    """Manga model.

    Attributes:
        id_manga (str): Manga's id.
        title (str): Manga's title.
        author (str): Manga's author.
        description (str): Manga's description.
        price (int): Manga's price.
        stock (int): Manga's stock.
        image (str): Manga's image.
        genre (str): Manga's genre.
        publisher (str): Manga's publisher.
        publication_date (datetime): Manga's publication date.
        supplier (str): Manga's supplier. Foreign key to Supplier model.
    """
    __tablename__ = "mangas"

    id_manga = Column(String(35), primary_key=get_uuid)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    publisher = Column(String(50), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    supplier = Column(String(35), ForeignKey("suppliers.id_supplier"), nullable=False)
    order = relationship("Order", backref="manga", lazy=True)
    review = relationship("Review", backref="manga", lazy=True)

    def __init__(self, title, author, description, price, stock, image, genre, publisher, publication_date, supplier):
        """Manga constructor."""
        self.title = title
        self.author = author
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.genre = genre
        self.publisher = publisher
        self.publication_date = publication_date
        self.supplier = supplier

    def get_dict(self):
        """Get manga's data in a dictionary.

        Returns:
            dict: Manga's data.
        """
        return {
            "id_manga": self.id_manga,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
            "genre": self.genre,
            "publisher": self.publisher,
            "publication_date": self.publication_date,
            "supplier": self.supplier
        }


class Supplier(Model):
    """Supplier model.

    Attributes:
        id_supplier (str): Supplier's id.
        name (str): Supplier's name.
        contact_phone (str): Supplier's contact phone.
        email (str): Supplier's email.
    """
    __tablename__ = "suppliers"

    id_supplier = Column(String(35), primary_key=get_uuid)
    name = Column(String(50), nullable=False)
    contact_phone = Column(String(9), nullable=False)
    email = Column(String(100), nullable=False)
    manga = relationship("Manga", backref="supplier", lazy=True)

    def __init__(self, name, contact_phone, email):
        """Supplier constructor."""
        self.name = name
        self.contact_phone = contact_phone
        self.email = email

    def get_dict(self):
        """Get supplier's data in a dictionary.

        Returns:
            dict: Supplier's data.
        """
        return {
            "id_supplier": self.id_supplier,
            "name": self.name,
            "contact_phone": self.contact_phone,
            "email": self.email
        }


class Review(Model):
    """Review model.

    Attributes:
        user (str): User who writes the review. Foreign key to User model.
        manga (str): Manga which is reviewed. Foreign key to Manga model.
        comment (str): Review's comment.
        rating (str): Review's rating.
        date (datetime): Review's date.
    """
    __tablename__ = "reviews"

    user = Column(String(35), ForeignKey("users.id_user"), primary_key=True, nullable=False)
    manga = Column(String(35), ForeignKey("mangas.id_manga"), primary_key=True, nullable=False)
    comment = Column(Text, nullable=False)
    rating = Column(String(5), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, user, manga, comment, rating):
        """Review constructor."""
        self.user = user
        self.manga = manga
        self.comment = comment
        self.rating = rating

    def get_dict(self):
        """Get review's data in a dictionary.

        Returns:
            dict: Review's data.
        """
        return {
            "user": self.user,
            "manga": self.manga,
            "comment": self.comment,
            "rating": self.rating,
            "date": self.date
        }


class Order(Model):
    """Order model.

    Attributes:
        id_order (str): Order's id.
        date (datetime): Order's date.
        status (str): Order's status. It is an enum: pending, sent, preparing or cancelled.
        total_price (int): Order's total price.
        user (str): User who makes the order. Foreign key to User model.
        address (str): Address where the order is sent. Foreign key to Address model.
    """
    __tablename__ = "orders"

    id_order = Column(String(35), primary_key=get_uuid)
    date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(Enum("pending", "sent", "preparing", "cancelled", name="order_status"), nullable=False,
                    default="pending")
    total_price = Column(Integer, nullable=False)
    user = Column(String(35), ForeignKey("users.id_user"), nullable=False)
    address = Column(String(35), ForeignKey("addresses.id_address"), nullable=False)

    def __init__(self, date, status, total_price, user, address):
        self.date = date
        self.status = status
        self.total_price = total_price
        self.user = user
        self.address = address

    def get_dict(self):
        """Get order's data in a dictionary.

        Returns:
            dict: Order's data.
        """
        return {
            "id_order": self.id_order,
            "date": self.date,
            "status": self.status,
            "total_price": self.total_price,
            "user": self.user,
            "address": self.address
        }


class OrderManga(Model):
    """OrderManga model.

    Model needed to represent the many-to-many relationship between Order and Manga models.

    Attributes:
        id_order (str): Order's id. Foreign key to Order model.
        id_manga (str): Manga's id. Foreign key to Manga model.
        quantity (int): Manga's quantity.
    """
    __tablename__ = "orders_mangas"

    id_order = Column(String(35), ForeignKey("orders.id_order"), primary_key=True, nullable=False)
    id_manga = Column(String(35), ForeignKey("mangas.id_manga"), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, id_order, id_manga, quantity):
        """OrderManga constructor."""
        self.id_order = id_order
        self.id_manga = id_manga
        self.quantity = quantity

    def get_dict(self):
        """Get OrderManga's data in a dictionary.

        Returns:
            dict: OrderManga's data.
        """
        return {
            "id_order": self.id_order,
            "id_manga": self.id_manga,
            "quantity": self.quantity
        }


class New(Model):
    """New model.

    Attributes:
        id_new (str): New's id.
        title (str): New's title.
        description (str): New's description.
        category (str): New's category. It is an enum: manga, anime or japan.
        date (datetime): New's date.
    """
    __tablename__ = "news"

    id_new = Column(String(35), primary_key=get_uuid)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum("manga", "anime", "japan", name="new_category"), nullable=False)
    image = Column(String(100), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, title, description, category):
        """New constructor."""
        self.title = title
        self.description = description
        self.category = category

    def get_dict(self):
        """Get new's data in a dictionary.

        Returns:
            dict: New's data.
        """
        return {
            "id_new": self.id_new,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "date": self.date
        }
