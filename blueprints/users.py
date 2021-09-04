from flask import Blueprint, request, render_template, session, redirect, url_for, flash

from managers.users import create_user, get_user

USERS_BLUEPRINT = Blueprint('users', __name__)
TASKS_INDEX = 'tasks.index'
USERS_LOGIN = 'users.login'


@USERS_BLUEPRINT.route('', methods=['POST'])
def index():
    ...


@USERS_BLUEPRINT.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('psw')
        password_repeat = request.form.get('psw-repeat')
        user_type = request.form.get('user-type')

        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        age = request.form.get('age')

        domain = request.form.get('domain') or 'GENERAL'

        if password == password_repeat:
            try:
                create_user(username=username, password=password, first_name=first_name, last_name=last_name, age=age,
                            domain=domain, user_type=user_type)
            except Exception as err:
                flash('Username already exists, please try with a different one')
                return redirect(url_for('users.register_user'))
            user = get_user(username, password)
            session['user_idx'] = user.idx
            session['username'] = user.username
            session['user_type'] = user.user_type.value
            if session.get('user_type') == 'DOCTOR':
                return redirect(url_for('doctors.appointments'))
            elif session.get('user_type') == 'ADMIN':
                return redirect(url_for('admin.doctors'))
            elif session.get('user_type') == 'PATIENT':
                return redirect(url_for('patients.doctors'))
        else:
            flash('Passwords do not match')
            return redirect(url_for('users.register_user'))


@USERS_BLUEPRINT.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_idx' in session:
        if session.get('user_type') == 'DOCTOR':
            return redirect(url_for('doctors.appointments'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('psw')
        try:
            user = get_user(username, password)
            if user:
                session['user_idx'] = user.idx
                session['username'] = user.username
                session['user_type'] = user.user_type.value
                if session.get('user_type') == 'DOCTOR':
                    return redirect(url_for('doctors.appointments'))
                elif session.get('user_type') == 'ADMIN':
                    return redirect(url_for('admin.doctors'))
                elif session.get('user_type') == 'PATIENT':
                    return redirect(url_for('patients.doctors'))
            else:
                flash('Wrong username or password')
                return redirect(url_for(USERS_LOGIN))
        except AttributeError:
            flash('Wrong username or password')
            return redirect(url_for(USERS_LOGIN))


@USERS_BLUEPRINT.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        if 'user_type' in session:
            del session['user_type']
        if 'user_idx' in session:
            del session['user_idx']
        if 'username' in session:
            del session['username']

    except KeyError:
        return redirect(url_for(USERS_LOGIN))
    return redirect(url_for(USERS_LOGIN))
