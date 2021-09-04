from database.models.tables.slots import Slot
from database.models.tables.appointments import Appointment
from managers.appointment import create_appointment
from uuid import uuid4
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def create_slot(doctor_id, date, slots):
    Slot.create(idx=str(uuid4()), doctor_id=doctor_id, date=datetime.strptime(date, DATE_FORMAT),
                slot1=slots[0] or 'False', slot2=slots[1] or 'False',
                slot3=slots[2] or 'False',
                slot4=slots[3] or 'False')


def get_slot_by_doctor_id(doctor_id):
    return Slot.get_by_doctor_id(doctor_id)


def book_slot(slot_id, doctor_id, patient_id, slot_number):
    slot = Slot.get(slot_id)
    if slot_number == 'Slot1':
        slot.slot1 = patient_id
    elif slot_number == 'Slot2':
        slot.slot2 = patient_id
    elif slot_number == 'Slot3':
        slot.slot3 = patient_id
    elif slot_number == 'Slot4':
        slot.slot4 = patient_id
    slot.save()
    create_appointment(doctor_id=doctor_id, patient_id=patient_id, slot_number=slot_number, date=slot.date)
