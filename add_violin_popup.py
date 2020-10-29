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
from models.violin import Violin

class AddViolinPopup(tk.Frame):
    """ Popup Frame to Add a Violin """

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
        ttk.Label(self, text="Primary Wood:").grid(row=5, column=1)
        self._primary_wood = ttk.Entry(self)
        self._primary_wood.grid(row=5, column=2)
        ttk.Label(self, text="Size:").grid(row=6, column=1)
        self._size = ttk.Entry(self)
        self._size.grid(row=6, column=2)
        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

    def _submit_cb(self):
        """ Submit the new violin """
        data = {}
        data['brand_name'] = self._brand_name.get()
        data['model_num'] = self._model_num.get()
        data['manufacture_date'] = self._manufacture_date.get()
        data['price'] = self._price.get()
        data['primary_wood'] = self._primary_wood.get()
        data['size'] = self._size.get()
        data['type'] = 'violin'
        print(data)

        r = requests.post("http://127.0.0.1:5000/store/instrument", json=(data))
        if r.status_code == 200:
            print("New violin has been added.")
            self._close_cb()
        else:
            print(r.text)
            tk.messagebox.showerror(title="Error", message=r.text)
