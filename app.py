from logging import FileHandler, Formatter

from flask import abort, Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from auth import auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(auth)
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/newsletter')
def newsletter():
    return abort(404)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


@app.cli.command()
def migrate_database():
    from auth import models
    db.create_all()
    models.db.create_all()

    print('Database created')


@app.cli.command()
def reset_database():
    from auth import models
    db.drop_all()
    models.db.drop_all()

    print('Database removed')


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
