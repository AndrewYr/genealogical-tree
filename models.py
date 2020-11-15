from peewee import *

db = SqliteDatabase('people.db')


class PersonModel:
    class Meta:
        database = db # This model uses the "people.db" database.

    # id = CharField()
    # family_id =
    # parent_id =
    # name =
    # surname =
    # patronymic =
    # birthday =
