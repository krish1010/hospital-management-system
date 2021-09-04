from flask import Blueprint, render_template, session

from database.models.tables.appointments import Appointment
from database.models.tables.doctors import Doctor
from managers.slot import get_slot_by_doctor_id, book_slot

PATIENTS_BLUEPRINT = Blueprint('patients', __name__)
USERS_LOGIN = 'users.login'


@PATIENTS_BLUEPRINT.route('', methods=['POST'])
def index():
    ...


@PATIENTS_BLUEPRINT.route('/doctors', methods=['GET'])
def doctors():
    all_doctors = Doctor.get_all_doctors()
    context = {
        'all_doctors': all_doctors
    }
    return render_template('patient_all_doctors.html', **context)


@PATIENTS_BLUEPRINT.route('/doctors/<idx>', methods=['GET'])
def view_doctor_slots(idx):
    slots = get_slot_by_doctor_id(idx)
    context = {
        'slots': slots,
        'doctor_id': idx
    }
    return render_template('doctor_all_slots.html', **context)


@PATIENTS_BLUEPRINT.route('/doctors/<doctor_id>/<patient_id>/book/<slot_id>/<slot_number>', methods=['GET'])
def book(doctor_id, patient_id, slot_id, slot_number):
    book_slot(slot_id, doctor_id, patient_id, slot_number)
    slots = get_slot_by_doctor_id(doctor_id)
    context = {
        'slots': slots,
        'doctor_id': doctor_id
    }
    return render_template('doctor_all_slots.html', **context)


@PATIENTS_BLUEPRINT.route('/appointments', methods=['GET'])
def appointments():
    all_appointments = Appointment.get_by_patient_id(session.get('user_idx'))
    context = {
        'all_appointments': all_appointments
    }
    return render_template('doctor_all_appointments.html', **context)


@PATIENTS_BLUEPRINT.route('/appointments/<idx>', methods=['GET'])
def view_appointment(idx):
    prescription_text = Appointment.get(idx).prescription_text
    context = {
        'prescription_text': prescription_text,
        'appointment_idx': idx
    }
    return render_template('view_prescription.html', **context)
