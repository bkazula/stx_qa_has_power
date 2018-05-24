from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return func(*args, **kwargs)
        else:
            flash('Musisz się zalogować', 'info')
            return redirect(url_for('auth.login'))
    return wrap