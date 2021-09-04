from database.db import db


class Slot(db.Model):
    __tablename__ = 'slots'

    idx = db.Column(db.String, primary_key=True)
    doctor_id = db.Column(db.String)
    slot1 = db.Column(db.String)
    slot2 = db.Column(db.String)
    slot3 = db.Column(db.String)
    slot4 = db.Column(db.String)
    date = db.Column(db.Date)

    @classmethod
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_doctor_id(cls, idx: str):
        slot = cls.query.filter_by(doctor_id=idx).all()
        return slot

    @classmethod
    def get_by_patient_id(cls, idx: str):
        user = cls.query.filter_by(idx=idx)
        return user

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
