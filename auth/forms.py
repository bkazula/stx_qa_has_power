import re
from sqlalchemy.orm.exc import NoResultFound
from wtforms import Form, PasswordField, StringField, validators

from .models import User


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(
        min=5, max=50, message='To pole powinno mieć min 5 max 50 znaków'
    )])
    email = StringField(
        'Email',
        [validators.DataRequired(message='To pole jest wymagane'),
         validators.Email(message='Niepoprawny adres email')]
    )
    password = PasswordField('Password', [
        validators.DataRequired(message='To pole jest wymagane'),
        validators.Length(
            min=12,
            max=17,
            message='Hasło musi mieć co najmniej 12 znaków i nie więcej niz 17'
        ),
    ])
    confirm = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Podane hasła są rózne')
    ])

    def validate_password(self, field):
        value: str = field.data
        rules = [
            re.match('^([A-Z].*|.*[A-Z])$', value), # Wielka litera na początku lub końcu
            re.match('.*[0-9].*', value), # Jedna cyfra
            re.match('.*[a-z].*[a-z].*', value), # Dwie małe litery w dowolnym miejscu
            re.match('.+[^\w\s].*', value), # Co najmniej jeden znak specjalny, nie na początku
        ]
        for rule in rules:
            if not rule:
                raise validators.ValidationError(
                    """Hasło musi zawierać minimum jedną duzą literę, 2 cyfry,
                     znak specjalny i małe litery"""
                     )

    def validate_email(self, field):
        try:
            User.query.filter_by(email=field.data).one()
            raise validators.ValidationError(
                'Nie mozna zarejestrować podanego adresu email')
        except NoResultFound:
            pass


class UserLoginForm(Form):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField(
        'Password', validators=[validators.DataRequired()]
    )
