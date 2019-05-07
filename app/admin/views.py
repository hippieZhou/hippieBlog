from . import bp

from app import login_manager
from app.models import User
from app.forms import LoginForm

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user


@login_manager.user_loader
def load_usesr(user_id: int):
    user = User.query.get(user_id)
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return 'Unauthorized'


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    else:
        return render_template('/admin/index.html', title='Admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        pwd = form.pwd.data
        user = User.query.filter_by(email=email).first()
        if user and user.name and user.email and user.check_password_hash(pwd):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('admin.index'))
        else:
            flash('E-mail/Password Is Error.', category='error')
    return render_template('/admin/login.html', title='Login', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
