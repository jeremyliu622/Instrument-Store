"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    A script to create tables
"""
from database import db
from models.violin import Violin
from models.piano import Piano
# from instrument_store import InstrumentStore


def create_db_tables():
    db.create_tables([Piano, Violin])
    
    # data for testing
    piano1 = Piano(brand_name="Yamaha", model_num="A14", manufacture_date="2020-04-09", price=123.556, piano_type="electric", num_of_keys=55)
    piano2 = Piano(brand_name="123", model_num="A14", manufacture_date="2020-04-09", price=123.556, piano_type="electric", num_of_keys=55)
    violin1 = Violin(brand_name="Poke", model_num="1D3", manufacture_date="2020-01-01", price=999.456, size="55/22", primary_wood="Oak")
    piano1.save()
    piano2.save()
    violin1.save()

