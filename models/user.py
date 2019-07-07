from datetime import datetime

from flask_bcrypt import generate_password_hash
from flask_login.mixins import UserMixin
from peewee import BooleanField, CharField, DateTimeField, IntegrityError

from models.base_model import BaseModel


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        db_table = "user"
        order_by = "-joined_at"  # negative means sort in decending order

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin,
            )
        except IntegrityError:
            raise ValueError("User already exists!")
