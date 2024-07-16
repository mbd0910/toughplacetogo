# models.py
from peewee import Model, CharField, IntegerField, PostgresqlDatabase
from config import DATABASE

db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    age = IntegerField()
