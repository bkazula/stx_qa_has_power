from flask import Blueprint, render_template, request, flash, redirect, url_for

from home.froms import ContactForm
from home.models import Contact, db

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/contact', methods=['GET'])
def contact():
    form = ContactForm(request.form)
    return render_template('pages/contact_form.html', form=form)


@home.route('/contact', methods=['POST'])
def contact_post():
    form = ContactForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        topic = form.topic.data
        message = form.message.data
        contact = Contact(name=name, email=email, topic=topic, message=message)
        db.session.add(contact)
        db.session.commit()
        flash('Twoja wiadomość została wysłana', 'success')
        return redirect(url_for('home.contact'))
    return render_template('pages/contact_form.html', form=form)

