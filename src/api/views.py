import logging
from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, session
from flask_login import login_required, current_user
from src.decorators import admin_required
from src.extensions import db
from src.database.models import User, Address, Manga, Supplier, Review, Order, OrderManga, New


view = Blueprint('view', __name__)


@view.route('/')
def home():
    try:
        mangas = db.session.query(Manga).order_by(Manga.added_date.desc()).limit(5).all()
        reviews = db.session.query(Review).order_by(Review.date.desc()).limit(6).all()

        return render_template('home.html', mangas=mangas, reviews=reviews), 200
    except Exception as error:
        flash('Error al obtener los mangas.', category='error')
        flash('Error al obtener las reseñas.', category='error')
        logging.error(error)

        return render_template('home.html', error=error), 500


@view.route('/sign_in', methods=['GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    return render_template('login.html')


@view.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    return render_template('sign_up.html')


@view.route('/products')
def products():
    try:
        mangas = db.session.query(Manga).order_by(Manga.added_date.desc()).all()

        return render_template('products.html', mangas=mangas), 200
    except Exception as error:
        flash('Error al obtener los mangas.', category='error')
        logging.error(error)

        return render_template('products.html', error=error), 500


@view.route('/product/<manga_id>', methods=['GET'])
def product(manga_id=None):
    try:
        manga = db.session.query(Manga).filter_by(id_manga=manga_id).first()

        if manga.reviews_manga:
            total_rating = 0
            for manga_review in manga.reviews_manga:
                total_rating += manga_review.rating
            average_rating = total_rating / len(manga.reviews_manga)
        else:
            average_rating = 0

        allow_review = False
        user_reviewed = False

        if not current_user.is_anonymous:
            user = db.session.query(User).filter_by(id_user=current_user.id_user).first()

            if user.has_payments():
                for payment in current_user.payments_user:
                    if not allow_review:
                        order = db.session.query(Order).filter_by(id_order=payment.order_payments[0].id_order).first()
                        for manga_in_order in order.orders_mangas_order:
                            if manga_in_order.id_manga == manga_id:
                                allow_review = True
                                if manga.reviews_manga:
                                    for review in manga.reviews_manga:
                                        if review.user == current_user.id_user:
                                            user_reviewed = review.get_dict()
                                break

        return render_template(
            'product.html', product=manga, reviews=manga.reviews_manga, rating=average_rating,
            allow_review=allow_review, user_reviewed=user_reviewed
        ), 200
    except Exception as error:
        flash('Error al obtener el manga.', category='error')
        logging.error(error)

        return render_template('product.html', error=error), 500


@view.route('/shopping_cart')
@login_required
def shopping_cart():
    mangas = []
    for id_manga, quantity in session['cart'].items():
        manga = db.session.query(Manga).filter_by(id_manga=id_manga).first()
        mangas.append({'manga': manga.get_dict(), 'quantity': quantity})
    return render_template('shopping_cart.html', products=mangas)


@view.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')


@view.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('view.home'))
    return render_template('profile.html')
