"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    A script to drop tables
"""
from database import db
from models.violin import Violin
from models.piano import Piano

def drop_db_tables():
    db.drop_tables([Piano, Violin])