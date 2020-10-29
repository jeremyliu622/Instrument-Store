from unittest import TestCase
from models.instrument_store import InstrumentStore
from models.piano import Piano
from models.violin import Violin
from peewee import SqliteDatabase


class TestInstrumentStore(TestCase):
    """ Unit tests for InstrumentStore """

    def setUp(self):
        """ Sets up an InstrumentStore object """
        self.db = SqliteDatabase("test.db")
        self.db.connect()
        self.db.create_tables([Piano, Violin])
        self.instrument_store1 = InstrumentStore("Tim's Music Shop")
        self.piano_data = {"brand_name": "Yamaha", "model_num": "B13", "manufacture_date": "2020-04-09",
                           "price": 123.55, "piano_type": "electric", "num_of_keys": 55, "type": "piano"}
        self.violin_data = {"brand_name": "Poke", "model_num": "1D3", "manufacture_date": "2020-01-01",
                            "price": 999.45, "size": "55/22", "primary_wood": "Oak", "type": "violin"}
        # self.piano1 = Piano(brand_name="123", model_num="A14", manufacture_date="2020-04-09", price=123.55,
        #                     piano_type="electric", num_of_keys=55)
        # self.violin1 = Violin(brand_name="Poke", model_num="1D3", manufacture_date="2020-01-01", price=999.45,
        #                       size="55/22", primary_wood="Oak")

    def tearDown(self):
        self.db.drop_tables([Piano, Violin])

    def test_init_valid(self):
        """ Checking parameter validation with the valid argument """
        instrument_store = InstrumentStore("Ming's Music Shop")
        self.assertIsNotNone(instrument_store)
        self.assertIsInstance(instrument_store, InstrumentStore)

    def test_init_invalid(self):
        """ Checking parameter validation with invalid argument """
        with self.assertRaises(ValueError):
            instrument_store = InstrumentStore("")
        with self.assertRaises(ValueError):
            instrument_store = InstrumentStore(123)


    def test_add_valid(self):
        """ Testing the add function with valid parameters """
        self.instrument_store1.add(self.piano_data)
        piano = Piano.select().where(Piano.brand_name == 'Yamaha').get()
        self.assertIsNotNone(piano)
        self.instrument_store1.add(self.violin_data)
        violin = Violin.select().where(Violin.brand_name == 'Poke').get()
        self.assertIsNotNone(violin)


    def test_add_invalid(self):
        """ Testing the add function with invalid parameters """
        piano_data1 = {"brand_name": "Yamaha", "model_num": "B13", "manufacture_date": "2020-04-09",
                      "price": 123.55, "piano_type": "electric", "num_of_keys": 55, "type": "sth"}
        violin_data1 = {"brand_name": "Poke", "model_num": "1D3", "manufacture_date": "20200101",
                       "price": 999.45, "size": "55/22", "primary_wood": "Oak", "type": "violin"}
        piano_data2 = {"brand_name": "Yamaha", "model_num": "B13", "manufacture_date": "2020-04-09",
                      "price": 123.55, "piano_type": "electric", "num_of_keys": "55.5", "type": "piano"}
        violin_data2 = {"brand_name": "Poke", "model_num": "1D3", "manufacture_date": "2020-01-01",
                       "price": "asd", "size": "55/22", "primary_wood": "Oak", "type": "violin"}
        with self.assertRaises(ValueError):
            self.instrument_store1.add(piano_data1)
        with self.assertRaises(ValueError):
            self.instrument_store1.add(violin_data1)
        with self.assertRaises(ValueError):
            self.instrument_store1.add(piano_data2)
        with self.assertRaises(ValueError):
            self.instrument_store1.add(violin_data2)

    def test_get_valid(self):
        """ Testing the get function with valid parameters """
        self.instrument_store1.add(self.piano_data)
        self.instrument_store1.add(self.violin_data)
        self.assertIsInstance(self.instrument_store1.get(1, 'piano'), dict)
        self.assertIsInstance(self.instrument_store1.get(1, 'violin'), dict)

    def test_get_invalid(self):
        """ Testing the get function with invalid parameters """
        self.instrument_store1.add(self.piano_data)
        self.instrument_store1.add(self.violin_data)
        with self.assertRaises(ValueError):
            self.instrument_store1.get(100, 'piano')
        with self.assertRaises(ValueError):
            self.instrument_store1.get(1, 'sth')
        with self.assertRaises(ValueError):
            self.instrument_store1.get(100, 'violin')

    def test_get_name(self):
        """ Testing the get_name function """
        self.assertEqual(self.instrument_store1.get_store_name(), "Tim's Music Shop")

    def test_get_all(self):
        """ Testing get_all function that retrieves all instruments in the form of a list """
        self.assertIsNotNone(self.instrument_store1.get_all())
        self.assertIsInstance(self.instrument_store1.get_all(), list)
        self.assertEqual(len(self.instrument_store1.get_all()), 0)

        self.instrument_store1.add(self.piano_data)
        self.assertEqual(len(self.instrument_store1.get_all()), 1)

        self.instrument_store1.add(self.violin_data)
        self.assertEqual(len(self.instrument_store1.get_all()), 2)

    def test_get_all_type_valid(self):
        """ Testing get_all_type function that retrieves all instruments of a type in the form of a list """
        self.assertIsNotNone(self.instrument_store1.get_all_by_type('piano'))
        self.assertIsInstance(self.instrument_store1.get_all_by_type('piano'), list)

        self.assertIsNotNone(self.instrument_store1.get_all_by_type('violin'))
        self.assertIsInstance(self.instrument_store1.get_all_by_type('violin'), list)

        self.assertEqual(len(self.instrument_store1.get_all_by_type('piano')), 0)
        self.assertEqual(len(self.instrument_store1.get_all_by_type('violin')), 0)

        self.instrument_store1.add(self.piano_data)
        self.assertEqual(len(self.instrument_store1.get_all_by_type('piano')), 1)

        self.instrument_store1.add(self.violin_data)
        self.assertEqual(len(self.instrument_store1.get_all_by_type('violin')), 1)

    def test_get_all_type_invalid(self):
        """ Testing get_all_type function that raise a ValueError if the type is wrong """
        with self.assertRaises(ValueError):
            self.instrument_store1.get_all_by_type('sth')

    def test_remove_instrument_by_id_valid(self):
        """ Testing remove_instrument_by_id with valid parameters """
        self.instrument_store1.add(self.piano_data)
        self.assertEqual(len(self.instrument_store1.get_all()), 1)
        self.instrument_store1.add(self.violin_data)
        self.assertEqual(len(self.instrument_store1.get_all()), 2)
        self.instrument_store1.remove_instrument_by_id(1, 'piano')
        self.assertEqual(len(self.instrument_store1.get_all()), 1)
        self.instrument_store1.remove_instrument_by_id(1, 'violin')
        self.assertEqual(len(self.instrument_store1.get_all()), 0)

    def test_remove_instrument_by_id_invalid(self):
        """ Testing remove_instrument_by_id with invalid parameters """
        with self.assertRaises(ValueError):
            self.instrument_store1.remove_instrument_by_id(100, 'piano')
        with self.assertRaises(ValueError):
            self.instrument_store1.remove_instrument_by_id(3, 'sth')
        with self.assertRaises(ValueError):
            self.instrument_store1.remove_instrument_by_id(100, 'violin')

    def test_get_stats(self):
        """ Testing get_stats return a dict"""
        self.assertIsInstance(self.instrument_store1.get_stats(), dict)
        self.instrument_store1.add(self.piano_data)
        self.instrument_store1.add(self.violin_data)
        self.assertIsInstance(self.instrument_store1.get_stats(), dict)

    def test_update_instrument_state_valid(self):
        """ Testing that the updated instrument is saved to database."""
        self.instrument_store1.add(self.piano_data)
        new_piano_data = {"brand_name": "Hamaya", "model_num": "B13", "manufacture_date": "2020-04-09",
                          "price": 123.55, "piano_type": "electric", "num_of_keys": 55, "type": "piano"}
        self.instrument_store1.update_instrument_state('piano', '1', new_piano_data)
        piano = Piano.select().where(Piano.id == 1).get()
        self.assertEqual(piano.brand_name, "Hamaya")

        self.instrument_store1.add(self.violin_data)
        new_violin_data = {"brand_name": "Kepo", "model_num": "1D3", "manufacture_date": "2020-01-01",
                            "price": 999.45, "size": "55/22", "primary_wood": "Oak", "type": "violin"}
        self.instrument_store1.update_instrument_state('violin', '1', new_violin_data)
        violin = Violin.select().where(Violin.id == 1).get()
        self.assertEqual(violin.brand_name, "Kepo")

    def test_update_instrument_state_invalid(self):
        """ Testing that the updated instrument can not be saved to database with invalid parameters."""
        self.instrument_store1.add(self.piano_data)
        new_piano_data1 = {"brand_name": "Hamaya", "model_num": "B13", "manufacture_date": "2020-04-09",
                          "price": 123.55, "piano_type": "electric", "num_of_keys": 55, "type": "piano"}
        new_piano_data2 = {"brand_name": "Hamaya", "model_num": "B13", "manufacture_date": "2020-04-09",
                          "price": 123.55, "piano_type": "electric", "num_of_keys": "asd", "type": "piano"}
        new_piano_data3 = {"brand_name": "Hamaya", "model_num": "B13", "manufacture_date": "2020-04-09",
                          "price": "asd", "piano_type": "electric", "num_of_keys": "55", "type": "piano"}
        with self.assertRaises(ValueError):
            self.instrument_store1.update_instrument_state('sth', '1', new_piano_data1)
        with self.assertRaises(ValueError):
            self.instrument_store1.update_instrument_state('piano', '1', new_piano_data2)
        with self.assertRaises(ValueError):
            self.instrument_store1.update_instrument_state('piano', '1', new_piano_data3)

    def test_validate_str(self):
        with self.assertRaises(ValueError):
            self.instrument_store1.validate_str(123, "name")
        with self.assertRaises(ValueError):
            self.instrument_store1.validate_str("", "name")

    def test_validate_date(self):
        with self.assertRaises(ValueError):
            self.instrument_store1.validate_date(20200101)

    def test_validate_positive_num(self):
        with self.assertRaises(ValueError):
            self.instrument_store1.validate_positive_num(-1, "number of keys")
