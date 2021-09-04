from flask import Blueprint, request, render_template, session, redirect, url_for

from database.models.tables.appointments import Appointment
from managers.appointment import update_prescription

DOCTORS_BLUEPRINT = Blueprint('doctors', __name__)
USERS_LOGIN = 'users.login'


@DOCTORS_BLUEPRINT.route('', methods=['POST'])
def index():
    ...


@DOCTORS_BLUEPRINT.route('/appointments', methods=['GET'])
def appointments():
    if session.get('user_type') == 'DOCTOR':
        all_appointments = Appointment.get_by_doctor_id(session.get('user_idx'))
        context = {
            'all_appointments': all_appointments
        }
        return render_template('doctor_all_appointments.html', **context)
    else:
        return redirect(url_for('users.logout'))


@DOCTORS_BLUEPRINT.route('/appointments/<idx>', methods=['POST'])
def prescription(idx):
    if session.get('user_type') == 'DOCTOR':
        prescription_text = request.form.get('prescription')
        update_prescription(idx, prescription_text)
        return redirect(url_for('doctors.appointments'))
    else:
        return redirect(url_for('users.logout'))
