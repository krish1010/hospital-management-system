from flask import Flask, redirect, url_for
from database.db import db

from blueprints.users import USERS_BLUEPRINT
from blueprints.doctor import DOCTORS_BLUEPRINT
from blueprints.admin import ADMIN_BLUEPRINT
from blueprints.patient import PATIENTS_BLUEPRINT

app = Flask(__name__)
app.config.from_pyfile('config/settings.staging.cfg')
db.init_app(app)

app.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')
app.register_blueprint(DOCTORS_BLUEPRINT, url_prefix='/doctors')
app.register_blueprint(ADMIN_BLUEPRINT, url_prefix='/admin')
app.register_blueprint(PATIENTS_BLUEPRINT, url_prefix='/patients')


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('users.register_user'))


if __name__ == '__main__':
    app.run(debug=True)
