from datetime import datetime, timedelta

from flask import (
    Blueprint,
    Response,
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
from auth.decorators import login_required
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
        flash('User created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('pages/register.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    form = UserLoginForm(request.form)
    invalid_counter = request.cookies.get('invalid_counter') or 0
    if int(invalid_counter) > 2 and 'last_login_try' in request.cookies:
        time = datetime.fromtimestamp(
            float(request.cookies.get('last_login_try')))
        minutes = {
            '3': 1,
            '4': 3,
            '5': 5,
            '6': 0,
        }
        delta = timedelta(minutes=minutes[invalid_counter] or 0)
        unlock_time = (time + delta).time()
        if unlock_time > datetime.now().time():
            flash('Nie możesz jeszcze podjąć próby logowania', 'danger')
            return redirect(url_for('auth.login'))
    try:
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).one()
            if check_password_hash(user.password, form.password.data):
                flash("Zostałeś zalogowany", 'success')
                session['email'] = request.form['email']
                return redirect(url_for('auth.dashboard'))
        raise NoResultFound
    except NoResultFound:
        resp = make_response() # type: Response
        error = None
        if invalid_counter:
            count = int(invalid_counter) + 1
            resp.set_cookie('invalid_counter', str(count))
            resp.set_cookie('last_login_try', str(datetime.now().timestamp()))
            if invalid_counter == '1':
                error = 'Niepoprawne dane logowania, spróbuj ponownie'
            elif invalid_counter == '2':
                error = 'Logowanie zostało zablokowane na 1 min'
            elif invalid_counter == '3':
                error = 'Logowanie zostało zablokowane na 3 min'
            elif invalid_counter == '4':
                error = 'Logowanie zostało zablokowane na 5 min'
            elif invalid_counter == '5':
                resp.delete_cookie('invalid_counter')
        else:
            error = 'Niepoprawne dane logowania, spróbuj ponownie'
            resp.set_cookie("invalid_counter", value='1')
        resp.response = render_template('pages/login.html', form=form, error=error)
        return resp


@auth.route('/login', methods=['GET'])
def login():
    form = UserLoginForm()
    return render_template('pages/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Zostałeś wylogowany!")
    return redirect(url_for('auth.login'))


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')