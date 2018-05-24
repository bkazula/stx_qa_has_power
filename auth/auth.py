from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from auth.forms import RegisterForm, UserLoginForm
from .models import User, db

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['GET'])
def register():
    form = RegisterForm()
    return render_template('pages/register.html', form=form)


@auth.route('/register', methods=['POST'])
def register_post():
    form = RegisterForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('auth.login'))
    return render_template('pages/register.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    form = UserLoginForm(request.form)
    try:
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).one()
            if check_password_hash(user.password, form.password.data):
                flash("You are now logged in")
                session['email'] = request.form['email']
                return redirect(url_for('auth.dashboard'))

        raise NoResultFound
    except NoResultFound:
        flash("Invalid credentials, try again.")
        return render_template('pages/login.html', form=form)

@auth.route('/login', methods=['GET'])
def login():
    form = UserLoginForm()
    return render_template('pages/login.html', form=form)


@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out!")
    return render_template('pages/logout.html')


@auth.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')
