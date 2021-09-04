from database.db import db


class Appointment(db.Model):
    __tablename__ = 'appointments'

    idx = db.Column(db.String, primary_key=True)
    doctor_id = db.Column(db.String, db.ForeignKey('users.idx'))
    patient_id = db.Column(db.String, db.ForeignKey('users.idx'))
    slot_number = db.Column(db.String)
    date = db.Column(db.Date)
    prescription_text = db.Column(db.Text, default='')
    doctor = db.relationship('User', backref=db.backref('appointment_doctor', cascade="delete, delete-orphan"),
                             lazy=True,
                             single_parent=True, foreign_keys='Appointment.doctor_id')
    patient = db.relationship('User', backref=db.backref('appointment_patient', cascade="delete, delete-orphan"),
                              lazy=True,
                              single_parent=True, foreign_keys='Appointment.patient_id')

    @classmethod
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    def get_by_doctor_id(cls, idx: str):
        appointment = cls.query.filter_by(doctor_id=idx).all()
        return appointment

    @classmethod
    def get_by_patient_id(cls, idx: str):
        appointments = cls.query.filter_by(patient_id=idx).all()
        return appointments

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()
