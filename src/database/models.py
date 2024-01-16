from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import ENUM
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.utils import get_uuid
from datetime import datetime
from enum import Enum


Model = db.Model
Column = db.mapped_column
Integer = db.Integer
Float = db.Float
String = db.String
Text = db.Text
Boolean = db.Boolean
ForeignKey = db.ForeignKey
DateTime = db.DateTime
relationship = db.relationship


class StatusEnum(Enum):
    """Enum for order status."""
    pending = "pending"
    sent = "sent"
    cancelled = "cancelled"


class CategoryEnum(Enum):
    """Enum for new category."""
    manga = "manga"
    anime = "anime"
    japan = "japan"


class PaymentMethodEnum(Enum):
    """Enum for payment method."""
    credit_card = "credit_card"
    paypal = "paypal"


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

    id_user = Column(String(35), primary_key=True, default=get_uuid)
    email = Column(String(100), unique=True, nullable=False)
    _password = Column(Text, nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=False)
    phone_number = Column(String(9), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    addresses_user = relationship("Address", back_populates="user_addresses")
    payments_user = relationship("Payment", back_populates="user_payments")
    reviews_user = relationship("Review", back_populates="user_reviews")
    wishlists_user = relationship("Wishlist", back_populates="user_wishlists")
    news_user = relationship("New", back_populates="user_news")

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

    def get_id(self) -> str:
        """Get user's id.

        Returns:
            str: User's id.
        """
        return self.id_user

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

    def has_payments(self) -> bool:
        """Check if a user has payments.

        Returns:
            bool: True if user has payments.
        """
        try:
            if self.payments_user:
                return True
            else:
                return False
        except Exception:
            return False

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
        user (str): User who owns the address. Foreign key to User model.
    """
    __tablename__ = "addresses"

    id_address = Column(String(35), primary_key=True, default=get_uuid)
    address_name = Column(String(20), nullable=False)
    address_line = Column(String(100), nullable=False)
    town = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    zip_code = Column(String(5), nullable=False)
    user = Column(String(35), ForeignKey("users.id_user"), nullable=False)
    user_addresses = relationship("User", back_populates="addresses_user")
    orders_address = relationship("Order", back_populates="address_orders")

    def __init__(self, address_name, address_line, town, city, zip_code, user):
        """Address constructor."""
        self.address_name = address_name
        self.address_line = address_line
        self.town = town
        self.city = city
        self.zip_code = zip_code
        self.user = user

    def __repr__(self):
        """Address representation.

        Returns:
            str: Address's line, town, city, zip code and country.
        """
        return f"{self.address_line}, {self.town}, {self.city}, {self.zip_code}"

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
        added_date (datetime): Manga's publication date.
        supplier (str): Manga's supplier. Foreign key to Supplier model.
    """
    __tablename__ = "mangas"

    id_manga = Column(String(35), primary_key=True, default=get_uuid)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    publisher = Column(String(50), nullable=False)
    added_date = Column(DateTime, nullable=False)
    supplier = Column(String(35), ForeignKey("suppliers.id_supplier"), nullable=False)
    supplier_mangas = relationship("Supplier", back_populates="mangas_supplier")
    reviews_manga = relationship("Review", back_populates="manga_reviews")
    wishlists_manga = relationship("Wishlist", back_populates="manga_wishlists")
    orders_mangas_manga = relationship("OrderManga", back_populates="manga_orders")

    def __init__(self, title, author, description, price, stock, image, genre, publisher, added_date, supplier):
        """Manga constructor."""
        self.title = title
        self.author = author
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.genre = genre
        self.publisher = publisher
        self.added_date = added_date
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
            "added_date": self.added_date,
            "supplier": self.supplier
        }


class Wishlist(Model):
    """Wishlist model.

    Attributes:
        user (str): User who owns the wishlist. Foreign key to User model.
        manga (str): Manga which is in the wishlist. Foreign key to Manga model.
    """
    __tablename__ = "wishlists"

    user = Column(String(35), ForeignKey("users.id_user"), primary_key=True, nullable=False)
    user_wishlists = relationship("User", back_populates="wishlists_user")
    manga = Column(String(35), ForeignKey("mangas.id_manga"), primary_key=True, nullable=False)
    manga_wishlists = relationship("Manga", back_populates="wishlists_manga")

    def __init__(self, user, manga):
        """Wishlist constructor."""
        self.user = user
        self.manga = manga

    def get_dict(self):
        """Get wishlist's data in a dictionary.

        Returns:
            dict: Wishlist's data.
        """
        return {
            "user": self.user,
            "manga": self.manga
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

    id_supplier = Column(String(35), primary_key=True, default=get_uuid)
    name = Column(String(50), nullable=False)
    contact_phone = Column(String(9), nullable=False)
    email = Column(String(100), nullable=False)
    mangas_supplier = relationship("Manga", back_populates="supplier_mangas")

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
    user_reviews = relationship("User", back_populates="reviews_user")
    manga = Column(String(35), ForeignKey("mangas.id_manga"), primary_key=True, nullable=False)
    manga_reviews = relationship("Manga", back_populates="reviews_manga")
    comment = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, user, manga, comment, rating, date):
        """Review constructor."""
        self.user = user
        self.manga = manga
        self.comment = comment
        self.rating = rating
        self.date = date

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


class Payment(Model):
    """Payment model.

    Attributes:
        id_payment (str): Payment's id.
        payment_date (datetime): Payment's date.
        payment_method (str): Payment's method. It is an enum: credit_card or paypal.
        total_price (int): Payment's total price.
        user (str): User who makes the payment. Foreign key to User model.
    """
    __tablename__ = "payments"

    id_payment = Column(String(35), primary_key=True, default=get_uuid)
    payment_date = Column(DateTime, nullable=False, default=datetime.now)
    payment_method = Column(ENUM(PaymentMethodEnum), nullable=False)
    total_price = Column(Float, nullable=False)
    user = Column(String(35), ForeignKey("users.id_user"), nullable=False)
    user_payments = relationship("User", back_populates="payments_user")
    order_payments = relationship("Order", back_populates="payment_orders")

    def __init__(self, payment_date, payment_method, total_price, user, id_payment=get_uuid()):
        """Payment constructor."""
        self.id_payment = id_payment
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.total_price = total_price
        self.user = user

    def get_dict(self):
        """Get payment's data in a dictionary.

        Returns:
            dict: Payment's data.
        """
        return {
            "id_payment": self.id_payment,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "total_price": self.total_price,
            "user": self.user
        }


class Order(Model):
    """Order model.

    Attributes:
        id_order (str): Order's id.
        date (datetime): Order's date.
        order_status (str): Order's status. It is an enum: pending, sent, preparing or cancelled.
        total_price (int): Order's total price.
        user (str): User who makes the order. Foreign key to User model.
        address (str): Address where the order is sent. Foreign key to Address model.
    """
    __tablename__ = "orders"

    id_order = Column(String(35), primary_key=True, default=get_uuid)
    date = Column(DateTime, nullable=False, default=datetime.now)
    order_status = Column(ENUM(StatusEnum), nullable=False, default="pending")
    total_price = Column(Float, nullable=False)
    payment = Column(String(35), ForeignKey("payments.id_payment"), nullable=False)
    payment_orders = relationship("Payment", back_populates="order_payments")
    address = Column(String(35), ForeignKey("addresses.id_address"), nullable=False)
    address_orders = relationship("Address", back_populates="orders_address")
    orders_mangas_order = relationship("OrderManga", back_populates="order_orders")

    def __init__(self, date, order_status, total_price, payment, address, id_order=get_uuid()):
        self.id_order = id_order
        self.date = date
        self.order_status = order_status
        self.total_price = total_price
        self.payment = payment
        self.address = address

    def get_dict(self):
        """Get order's data in a dictionary.

        Returns:
            dict: Order's data.
        """
        if self.order_status == StatusEnum.pending:
            status = "Pendiente"
        elif self.order_status == StatusEnum.sent:
            status = "Enviado"
        elif self.order_status == StatusEnum.cancelled:
            status = "Cancelado"
        else:
            status = "Preparando"

        return {
            "id_order": self.id_order,
            "date": self.date,
            "status": status,
            "total_price": self.total_price,
            "payment": self.payment,
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
    order_orders = relationship("Order", back_populates="orders_mangas_order")
    id_manga = Column(String(35), ForeignKey("mangas.id_manga"), primary_key=True, nullable=False)
    manga_orders = relationship("Manga", back_populates="orders_mangas_manga")
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
        user (str): User who writes the new. Foreign key to User model.
    """
    __tablename__ = "news"

    id_new = Column(String(35), primary_key=True, default=get_uuid)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(ENUM(CategoryEnum), nullable=False)
    image = Column(String(100), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    user = Column(String(35), ForeignKey("users.id_user"), nullable=False)
    user_news = relationship("User", back_populates="news_user")

    def __init__(self, title, description, category, date, user, image=None):
        """New constructor."""
        self.title = title
        self.description = description
        self.category = category
        self.image = image
        self.date = date
        self.user = user

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
            "date": self.date,
            "user": self.user
        }
