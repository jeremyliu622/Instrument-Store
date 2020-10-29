"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    Update instrument popup
"""
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pprint import pprint
from models.piano import Piano


class UpdateInstrumentPopup(tk.Frame):
    """ Popup Frame to Update a instrument """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        self._selectedInstrument = tk.StringVar(value="piano")
        tk.Radiobutton(self, text="Piano", command=self._toggle, variable=self._selectedInstrument, value="piano").grid(row=1, column=1)
        tk.Radiobutton(self, text="Violin", command=self._toggle, variable=self._selectedInstrument, value="violin").grid(row=1, column=2)

        ttk.Label(self, text="Instrument ID:").grid(row=2, column=1)
        self._id = ttk.Entry(self)
        self._id.grid(row=2, column=2)

        ttk.Label(self, text="Brand Name:").grid(row=3, column=1)
        self._brand_name = ttk.Entry(self)
        self._brand_name.grid(row=3, column=2)
        ttk.Label(self, text="Model No.:").grid(row=4, column=1)
        self._model_num = ttk.Entry(self)
        self._model_num.grid(row=4, column=2)
        ttk.Label(self, text="Manufacture Date:").grid(row=5, column=1)
        self._manufacture_date = ttk.Entry(self)
        self._manufacture_date.grid(row=5, column=2)
        ttk.Label(self, text="Price:").grid(row=6, column=1)
        self._price = ttk.Entry(self)
        self._price.grid(row=6, column=2)

        self._piano_label1 = ttk.Label(self, text="Piano Type:")
        self._piano_label1.grid(row=7, column=1)
        self._piano_type = ttk.Entry(self)
        self._piano_type.grid(row=7, column=2)

        self._violin_label1 = ttk.Label(self, text="Primary wood:")
        self._primary_wood = ttk.Entry(self)

        self._piano_label2 = ttk.Label(self, text="Numbers of Keys:")
        self._piano_label2.grid(row=8, column=1)
        self._num_of_keys = ttk.Entry(self)
        self._num_of_keys.grid(row=8, column=2)

        self._violin_label2 = ttk.Label(self, text="Size:")
        self._violin_size = ttk.Entry(self)

        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=9, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=9, column=2)

        self._toggle()

    def _submit_cb(self):
        """ Update instrument """
        try:
            data = {}
            data['brand_name'] = self._brand_name.get()
            data['model_num'] = self._model_num.get()
            data['manufacture_date'] = self._manufacture_date.get()
            data['price'] = self._price.get()
            if self._selectedInstrument.get() == 'piano':
                data['piano_type'] = self._piano_type.get()
                data['num_of_keys'] = self._num_of_keys.get()
                data['type'] = 'piano'
            elif self._selectedInstrument.get() == 'violin':
                data['primary_wood'] = self._primary_wood.get()
                data['size'] = self._violin_size.get()
                data['type'] = 'violin'
            self._validate_inputs(self._id.get())
            r = requests.put("http://127.0.0.1:5000/store/instrument/" + self._selectedInstrument.get() + '/' + self._id.get() , json=(data))
            print(r.status_code)
            print(r.text)
            if r.status_code == 200:
                print("Instrument has been updated.")
                self._close_cb()
            else:
                print(r.text)
                tk.messagebox.showerror(title="Wrong Input", message=r.text)
        except ValueError as e:
            tk.messagebox.showerror(title="Error", message=e)

    def _toggle(self):
        """ Toggle piano or violin fields """
        if (self._selectedInstrument.get()) == 'piano':
            self._violin_label1.grid_remove()
            self._primary_wood.grid_remove()
            self._violin_label2.grid_remove()
            self._violin_size.grid_remove()

            self._piano_label1.grid(row=7, column=1)
            self._piano_type.grid(row=7, column=2)
            self._piano_label2.grid(row=8, column=1)
            self._num_of_keys.grid(row=8, column=2)
        else:
            self._piano_label1.grid_remove()
            self._piano_type.grid_remove()
            self._piano_label2.grid_remove()
            self._num_of_keys.grid_remove()

            self._violin_label1.grid(row=7, column=1)
            self._primary_wood.grid(row=7, column=2)
            self._violin_label2.grid(row=8, column=1)
            self._violin_size.grid(row=8, column=2)

    def _validate_inputs(self, instrument_id):
        """ Validate input for instrument id """
        if not instrument_id:
            raise ValueError("Instrument_id cannot be empty")
        try:
            int(instrument_id)
        except:
            raise ValueError("ID must be an integer")