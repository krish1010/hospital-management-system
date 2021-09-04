from database.models.tables.users import User
from database.models.tables.doctors import Doctor
from database.models.enums.user_types import UserType
from database.models.enums.domains import Domain
from uuid import uuid4


def create_user(username, password, first_name, last_name, age, domain, user_type):
    idx = str(uuid4())
    if user_type == 'DOCTOR':
        Doctor.create(idx=idx, username=username, password=password, first_name=first_name,
                      last_name=last_name, domain=Domain(domain),
                      age=age, user_type=UserType(user_type))
    else:
        User.create(idx=idx, username=username, password=password, first_name=first_name, last_name=last_name,
                    age=age, user_type=UserType(user_type))


def get_user(username, password):
    user = User.get_by_username(username)
    if user.check_password(password):
        return user


def delete_user(idx):
    user = User.get(idx)
    user.delete()
