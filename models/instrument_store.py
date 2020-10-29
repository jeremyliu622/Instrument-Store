"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    This is a class representing an instrument store.
"""
from models.abstract_instrument import AbstractInstrument
from models.piano import Piano
from models.violin import Violin
from datetime import datetime


class InstrumentStore:

    def __init__(self, store_name):
        if not store_name:
            raise ValueError("Define store name")
        if type(store_name) is not str:
            raise ValueError("Store name should be a string")
        self._store_name = store_name

    def add(self, data) -> None:
        """ Create and add a new instrument to the database """
        self.validate_str(data["brand_name"], "brand_name")
        self.validate_str(data["model_num"], "model_num")
        self.validate_date(data["manufacture_date"])
        data["manufacture_date"] = datetime.strptime(data["manufacture_date"], '%Y-%m-%d').date()
        try:
            data["price"] = round(float(data["price"]), 2)
        except:
            raise ValueError('Price must be a float number.')
        self.validate_positive_num(data['price'], 'price')

        if data["type"] == 'violin':
            self.validate_str(data["primary_wood"], "primary_wood")
            self.validate_str(data["size"], "size")

            violin = Violin(brand_name=data["brand_name"], model_num=data["model_num"],
                            manufacture_date=data["manufacture_date"], price=data["price"], size=data["size"],
                            primary_wood=data["primary_wood"])
            violin.save()

        elif data["type"] == 'piano':
            self.validate_str(data["piano_type"], "piano_type")
            try:
                data['num_of_keys'] = int(data['num_of_keys'])
            except:
                raise ValueError('Numbers of keys must be an integer.')
            self.validate_positive_num(data['num_of_keys'], 'numbers of keys')

            piano = Piano(brand_name=data["brand_name"], model_num=data["model_num"],
                          manufacture_date=data["manufacture_date"], price=data["price"], piano_type=data["piano_type"],
                          num_of_keys=data["num_of_keys"])
            piano.save()
        else:
            raise ValueError("Invalid Type")

    def get(self, _id, _type) -> AbstractInstrument:
        """ Get an instrument of type and id from the database """
        if _type == "piano":
            try:
                instrument = Piano.select().where(Piano.id == _id).dicts().get()
            except:
                raise ValueError('Id does not exist.')
        elif _type == "violin":
            try:
                instrument = Violin.select().where(Violin.id == _id).dicts().get()
            except:
                raise ValueError('Id does not exist.')
        else:
            raise ValueError('Instrument type must be piano or violin.')
        instrument['manufacture_date'] = str(instrument['manufacture_date'])
        instrument['price'] = float(instrument['price'])
        return instrument


    def get_store_name(self) -> str:
        """ Return the name of this instrument store """
        return self._store_name

    def get_all(self):
        """ Return a list of all AbstractInstrument model in the inventory """
        instruments_list = []
        try:
            for piano in Piano.select().dicts():
                instruments_list.append(piano)
        except:
            print("No piano in the this store.")
        try:
            for violin in Violin.select().dicts():
                instruments_list.append(violin)
        except:
            print("No violin in the this store.")
        return instruments_list

    def get_all_by_type(self, instrument_type: str):
        """ Return a list of all AbstractInstrument objects with the given type"""
        instruments_list = list()
        if instrument_type == 'piano':
            try:
                for piano in Piano.select().dicts():
                    instruments_list.append(piano)
            except:
                print("No piano in the this store.")
        elif instrument_type == 'violin':
            try:
                for violin in Violin.select().dicts():
                    instruments_list.append(violin)
            except:
                print("No violin in this store.")
        else:
            raise ValueError('Instrument type must be piano or violin.')
        return instruments_list


    def remove_instrument_by_id(self, _id, _type) -> None:
        """ Remove instrument by the given id and type """
        self._check_existence(_type, _id)
        if _type == 'piano':
            try:
                delete_instrument = Piano.delete().where(Piano.id == _id)
                delete_instrument.execute()
            except:
                raise ValueError("Id does not exist.")
        elif _type == 'violin':
            try:
                delete_instrument = Violin.delete().where(Violin.id == _id)
                delete_instrument.execute()
            except:
                raise ValueError("Id does not exist.")
        else:
            raise ValueError('Instrument type must be piano or violin.')


    def get_stats(self) -> dict:
        """ Return stats, not implemented since EntityStats is not required for this project """
        output_dict = dict()
        output_dict["store_name"] = self.get_store_name()
        num_of_violins = 0
        num_of_pianos = 0

        if len(self.get_all()) > 0:
            for instrument in self.get_all():
                if instrument['instrument_type'] == 'piano':
                    num_of_pianos += 1
                elif instrument['instrument_type'] == 'violin':
                    num_of_violins += 1

        output_dict["number_of_violins"] = num_of_violins
        output_dict["number_of_pianos"] = num_of_pianos
        return output_dict

    def update_instrument_state(self, _type, _id, data) -> None:
        """ Update an instrument's state """
        self._check_existence(_type, _id)
        self.validate_str(data["brand_name"], "brand_name")
        self.validate_str(data["model_num"], "model_num")
        self.validate_date(data["manufacture_date"])
        data["manufacture_date"] = datetime.strptime(data["manufacture_date"], '%Y-%m-%d').date()
        try:
            data["price"] = round(float(data["price"]), 2)
        except:
            raise ValueError('Price must be a float number.')
        self.validate_positive_num(data['price'], 'price')
        if _type == 'violin':
            self.validate_str(data["primary_wood"], "primary_wood")
            self.validate_str(data["size"], "size")
            instrument = Violin.update(brand_name=data["brand_name"], model_num=data["model_num"],
                            manufacture_date=data["manufacture_date"], price=data["price"], size=data["size"],
                            primary_wood=data["primary_wood"]).where(Violin.id == _id)

        elif _type == 'piano':
            self.validate_str(data["piano_type"], "piano_type")
            try:
                data['num_of_keys'] = int(data['num_of_keys'])
            except:
                raise ValueError('Numbers of keys must be an integer.')
            self.validate_positive_num(data['num_of_keys'], 'numbers of keys')
            instrument = Piano.update(brand_name=data["brand_name"], model_num=data["model_num"],
                          manufacture_date=data["manufacture_date"], price=data["price"], piano_type=data["piano_type"],
                          num_of_keys=data["num_of_keys"]).where(Piano.id == _id)
        else:
            raise ValueError("Invalid Type")
        instrument.execute()

    def _check_existence(self, _type, _id):
        """ Validate that an instrument with ID exists """
        if _type == 'piano':
            query = Piano.select().where(Piano.id == _id)
            if not query.exists():
                raise ValueError(f"Could not find piano with ID:{_id}")
        elif _type =='violin':
            query = Violin.select().where(Violin.id == _id)
            if not query.exists():
                raise ValueError(f"Could not find violin with ID:{_id}")

    @classmethod
    def validate_str(cls, _str, para_name):
        if not isinstance(_str, str) or not _str:
            raise ValueError(para_name + ' must be a string that is not empty.')

    @classmethod
    def validate_date(cls, date):
        """check the input date is a str"""
        if not isinstance(date, str):
            raise ValueError("Date must be a string with the format 'yyyy-mm-dd'.")

    @classmethod
    def validate_positive_num(cls, num, para_name):
        """check the price is a float number and bigger than 0"""
        if num <= 0:
            raise ValueError(para_name + ' must be a number greater than 0.')
