"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
"""
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pprint import pprint
from models.piano import Piano


class AddPianoPopup(tk.Frame):
    """ Popup Frame to Add a Piano """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        ttk.Label(self, text="Brand Name:").grid(row=1, column=1)
        self._brand_name = ttk.Entry(self)
        self._brand_name.grid(row=1, column=2)
        ttk.Label(self, text="Model No.:").grid(row=2, column=1)
        self._model_num = ttk.Entry(self)
        self._model_num.grid(row=2, column=2)
        ttk.Label(self, text="Manufacture Date:").grid(row=3, column=1)
        self._manufacture_date = ttk.Entry(self)
        self._manufacture_date.grid(row=3, column=2)
        ttk.Label(self, text="Price:").grid(row=4, column=1)
        self._price = ttk.Entry(self)
        self._price.grid(row=4, column=2)
        ttk.Label(self, text="Piano Type:").grid(row=5, column=1)
        self._piano_type = ttk.Entry(self)
        self._piano_type.grid(row=5, column=2)
        ttk.Label(self, text="Numbers of Keys:").grid(row=6, column=1)
        self._num_of_keys = ttk.Entry(self)
        self._num_of_keys.grid(row=6, column=2)
        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

    def _submit_cb(self):
        """ Submit the new piano """
        data = {}
        data['brand_name'] = self._brand_name.get()
        data['model_num'] = self._model_num.get()
        data['manufacture_date'] = self._manufacture_date.get()
        data['price'] = self._price.get()
        data['piano_type'] = self._piano_type.get()
        data['num_of_keys'] = self._num_of_keys.get()
        data['type'] = 'piano'
        print(data)

        r = requests.post("http://127.0.0.1:5000/store/instrument", json=(data))
        print(r.status_code)
        print(r.text)
        if r.status_code == 200:
            print("New piano has been added.")
            self._close_cb()
        else:
            print(r.text)
            tk.messagebox.showerror(title="Wrong Input", message=r.text)





