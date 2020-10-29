from peewee import SqliteDatabase

db = SqliteDatabase("instrument_store.db")
db.connect()
