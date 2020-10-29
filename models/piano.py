"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
"""
from models.abstract_instrument import AbstractInstrument
from peewee import CharField, IntegerField 


class Piano(AbstractInstrument):
    """ A model that represents a piano """
    piano_type = CharField()
    num_of_keys = IntegerField()
    instrument_type = CharField(default='piano')

    