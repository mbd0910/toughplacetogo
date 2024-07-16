from datetime import datetime
from peewee import CharField, DateTimeField, PostgresqlDatabase
from playhouse.signals import pre_save, Model
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


class TimestampableModel(BaseModel):
    created_at = DateTimeField()
    updated_at = DateTimeField()


class Team(TimestampableModel):
    name = CharField()


@pre_save(sender=TimestampableModel)
def on_save_handler(model_class, instance, created):
    if created:
        instance.created_at = datetime.now()
    instance.updated_at = datetime.now()
