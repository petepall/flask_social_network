from pathlib import Path

from peewee import Model, SqliteDatabase

DB = SqliteDatabase(Path("db/social.db").resolve())


class BaseModel(Model):
    class Meta:
        db = DB
