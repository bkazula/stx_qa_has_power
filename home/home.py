from flask import Blueprint, render_template, request, flash, redirect, url_for, g

from home.froms import ContactForm
from home.models import Contact, db
from auth.decorators import login_required

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/contact', methods=['GET'])
def contact():
    data = {
        'name': g.user.name if 'user' in g else '',
        'email': g.user.email if 'user' in g else '',
    }
    form = ContactForm(**data)
    return render_template('pages/home/contact_form.html', form=form)


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
    return render_template('pages/home/contact_form.html', form=form)


@home.route('/about')
@login_required
def about():
    return render_template('pages/home/about.html')


@home.route('/privacy-policy')
def privacy_policy():
    return render_template('pages/home/privacy_policy.html')
