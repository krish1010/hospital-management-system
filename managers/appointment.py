from uuid import uuid4

from database.models.tables.appointments import Appointment


def create_appointment(doctor_id, patient_id, slot_number, date):
    Appointment.create(idx=str(uuid4()), doctor_id=doctor_id, patient_id=patient_id,
                       slot_number=slot_number, date=date)


def update_prescription(appointment_idx, prescription_text):
    appointment = Appointment.get(appointment_idx)
    appointment.prescription_text = prescription_text
    appointment.save()
