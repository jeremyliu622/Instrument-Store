"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    This is a class representing an abstract instrument.
"""
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField, DecimalField, BooleanField
from database import db


class AbstractInstrument(Model):
    """ A model representing an abstract instrument """
    brand_name = CharField()
    model_num = CharField()
    manufacture_date = DateField()
    price = DecimalField()
    is_sold = BooleanField(default=False)

    class Meta:
        database = db