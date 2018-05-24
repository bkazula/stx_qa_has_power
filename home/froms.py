from wtforms import Form, StringField, validators, TextAreaField


class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=5, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    topic = StringField('Topic', [validators.Length(max=50)])
    message = TextAreaField('Message', [validators.Length(max=255)])
