"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
"""
from models.abstract_instrument import AbstractInstrument
from peewee import CharField


class Violin(AbstractInstrument):
    """ A model that represents a violin """
    size = CharField()
    primary_wood = CharField()
    instrument_type = CharField(default='violin')


