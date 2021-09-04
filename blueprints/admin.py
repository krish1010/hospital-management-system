from flask import Blueprint, request, render_template, redirect, url_for, flash, session

from database.models.tables.doctors import Doctor
from managers.slot import get_slot_by_doctor_id, create_slot
from managers.users import create_user, delete_user

ADMIN_BLUEPRINT = Blueprint('admin', __name__)
USERS_LOGIN = 'users.login'


@ADMIN_BLUEPRINT.route('', methods=['POST'])
def index():
    ...


@ADMIN_BLUEPRINT.route('/doctors', methods=['GET'])
def doctors():
    if session.get('user_type') == 'ADMIN':
        all_doctors = Doctor.get_all_doctors()
        context = {
            'all_doctors': all_doctors
        }
        return render_template('admin_all_doctors.html', **context)
    else:
        return redirect(url_for('users.logout'))


@ADMIN_BLUEPRINT.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if session.get('user_type') == 'ADMIN':
        if request.method == 'GET':
            return render_template('admin_add_doctor.html')
        else:
            username = request.form.get('username')
            password = request.form.get('psw')
            password_repeat = request.form.get('psw-repeat')
            user_type = 'DOCTOR'

            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            age = request.form.get('age')

            domain = request.form.get('domain') or 'GENERAL'

            if password == password_repeat:
                try:
                    create_user(username=username, password=password, first_name=first_name, last_name=last_name,
                                age=age,
                                domain=domain, user_type=user_type)
                    return redirect(url_for('admin.doctors'))
                except Exception as err:
                    flash('Username already exists, please try with a different one')
                    return redirect(url_for('admin.add_doctor'))
            else:
                flash('Passwords do not match')
                return redirect(url_for('users.register_user'))
    else:
        return redirect(url_for('users.logout'))


@ADMIN_BLUEPRINT.route('/delete/<idx>', methods=['GET'])
def delete(idx):
    if session.get('user_type') == 'ADMIN':
        delete_user(idx)
        return redirect(url_for('admin.doctors'))
    else:
        return redirect(url_for('users.logout'))


@ADMIN_BLUEPRINT.route('/doctors/<idx>', methods=['GET'])
def view_doctor_slots(idx):
    if session.get('user_type') == 'ADMIN':
        slots = get_slot_by_doctor_id(idx)
        context = {
            'slots': slots,
            'doctor_id': idx
        }
        return render_template('doctor_all_slots.html', **context)
    else:
        return redirect(url_for('users.logout'))


@ADMIN_BLUEPRINT.route('/doctors/<idx>/add_slot', methods=['GET', 'POST'])
def add_slot(idx=None):
    if session.get('user_type') == 'ADMIN':
        if request.method == 'GET':
            return render_template('doctor_add_slot.html', **{'idx': idx})
        else:
            date = request.form.get('date')
            slot1, slot2, slot3, slot4 = request.form.get('slot1'), request.form.get('slot2'), request.form.get(
                'slot3'), request.form.get('slot4')
            create_slot(doctor_id=idx, date=date, slots=[slot1, slot2, slot3, slot4])
            return redirect(url_for('admin.view_doctor_slots', idx=idx))
    else:
        return redirect(url_for('users.logout'))
