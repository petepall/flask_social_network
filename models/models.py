from datetime import datetime

from peewee import BooleanField, CharField, DateTimeField
from models.base_model import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        db_table = "user"
        order_by = "-joined_at"  # negative means sort in decending order
