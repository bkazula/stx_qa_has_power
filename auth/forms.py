import re
from sqlalchemy.orm.exc import NoResultFound
from wtforms import Form, PasswordField, StringField, validators

from .models import User


class RegisterForm(Form):
    name = StringField('Name')
    email = StringField(
        'Email',
        [validators.DataRequired(message='To pole jest wymagane'),
         validators.Email(message='Niepoprawny adres email')]
    )
    password = PasswordField('Password', [
        validators.DataRequired(message='To pole jest wymagane'),
    ])
    confirm = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Podane hasła są rózne')
    ])

    def validate_password(self, field):
        value: str = field.data
        
        if not re.match('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9].*?[0-9])(?=.*?[#?!@$%^&*-]).{12,17}$', value):
            raise validators.ValidationError(
                'Hasło musi składać się od 12 do 17 znaków i zawierać minimum jedną duzą literę, 2 cyfry, '
                'znak specjalny i małe litery'
                )

        if False:
            rules = [
                re.match('^([A-Z].*|.*[A-Z])$', value), # Wielka litera na początku lub końcu
                re.match('.*[0-9].*', value), # Jedna cyfra
                re.match('.*[a-z].*[a-z].*', value), # Dwie małe litery w dowolnym miejscu
                re.match('.+[^\w\s].*', value), # Co najmniej jeden znak specjalny, nie na początku
            ]
            for rule in rules:
                if not rule:
                    raise validators.ValidationError(
                        'Hasło musi zawierać minimum jedną duzą literę, 2 cyfry, '
                        'znak specjalny i małe litery'
                        )

    def validate_email(self, field):
        value: str = field.data

        if re.match('.*\.{1,}.*\@.*', value):
            raise validators.ValidationError('Niepoprawny adres email')

        if False:
            try:
                User.query.filter_by(email=field.data).one()
                raise validators.ValidationError(
                    'Nie mozna zarejestrować podanego adresu email')
            except NoResultFound:
                pass

    def validate_name(self, field):
        value: str = field.data

        if len(value) > 60:
            raise Exception
            
        if len(value) > 50 or len(value) < 4:
            raise validators.ValidationError('To pole powinno mieć od 5 do 50 znaków')


class UpdateUserForm(Form):
    name = StringField('Name', [validators.Length(
        min=5, max=50, message='To pole powinno mieć od 5 do 50 znaków'
    )])
    email = StringField(
        'Email',
        [validators.DataRequired(message='To pole jest wymagane'),
         validators.Email(message='Niepoprawny adres email')]
    )


class UserLoginForm(Form):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField(
        'Password', validators=[validators.DataRequired()]
    )


class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', [
        validators.DataRequired(message='To pole jest wymagane'),
    ])
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
