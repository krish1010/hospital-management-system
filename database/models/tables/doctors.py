from database.db import db
from ..enums.domains import Domain
from ..enums.user_types import UserType
from ..tables.users import User


class Doctor(db.Model):
    __tablename__ = 'doctors'
    idx = db.Column(db.String, db.ForeignKey('users.idx'), primary_key=True)
    domain = db.Column(db.Enum(Domain))
    user = db.relationship('User', backref=db.backref('doctor', cascade="delete, delete-orphan"), lazy=True,
                           single_parent=True)

    @classmethod
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    def get_by_uid(cls, idx: str):
        user = cls.query.filter_by(idx=idx).first()
        return user

    @classmethod
    def get_by_username(cls, username: str):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def get_all_doctors(cls):
        doctors = cls.query.all()
        return doctors

    @classmethod
    def create(cls, **kwargs):
        user = User(idx=kwargs.get('idx'), username=kwargs.get('username'), password=kwargs.get('password'),
                    first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'),
                    age=kwargs.get('age'), user_type=UserType(kwargs.get('user_type')))
        instance = cls(idx=kwargs.get('idx'), domain=Domain(kwargs.get('domain')), user=user)
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
