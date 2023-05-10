from flask import render_template, Blueprint
from flask_login import login_required
from makise_app.decorators import admin_required


view = Blueprint('view', __name__)


@view.route('/')
def home():
    return render_template('home.html')


@login_required
@admin_required
@view.route('/admin')
def admin():
    return render_template('admin.html')


@login_required
@view.route('/profile')
def user():
    return render_template('profile.html')
