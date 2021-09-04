from database.db import db
from database.models.enums.user_types import UserType
import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    idx = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer, nullable=True)
    _password_hash = db.Column(db.String)
    user_type = db.Column(db.Enum(UserType))

    @property
    def password(self):
        raise AttributeError('Unreadable property password.')

    @password.setter
    def password(self, password):
        if password:
            self._password_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()
            ).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self._password_hash.encode())

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
