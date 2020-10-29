"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    Remove instrument popup window
"""
import requests
import tkinter as tk
from tkinter import ttk
import re


class RemoveInstrumentPopup(tk.Frame):
    """ Popup Frame to Remove a Instrument """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        ttk.Label(self, text="Instrument ID:").grid(row=1, column=1)
        self._instrument_id = ttk.Entry(self)
        self._instrument_id.grid(row=1, column=2)

        ttk.Label(self, text="Instrument Type:").grid(row=2, column=1)
        self._instrument_type = ttk.Entry(self)
        self._instrument_type.grid(row=2, column=2)

        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=4, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=4, column=2)

    def _submit_cb(self):
        """ Submit the Remove Instrument """
        instrument_id = self._instrument_id.get()
        instrument_type = self._instrument_type.get()
        try:
            self._validate_inputs(instrument_id, instrument_type)
            if self._accept_confirmation(instrument_id, instrument_type):
                r = requests.delete("http://127.0.0.1:5000/store/instrument/" + instrument_type + "/"  + instrument_id)
                if r.status_code == 200:
                    print(r.text)
                    self._close_cb()
                else:
                    print(r.text)
                    tk.messagebox.showerror(title="Error", message=r.text)
        except ValueError as e:
            tk.messagebox.showerror(title="Error", message=e)

    def _accept_confirmation(self, instrument_id, instrument_type):
        """ Confirmation popup """
        msg = f"Are you sure you want to delete {instrument_type} with ID: {instrument_id}"
        response = tk.messagebox.askyesno(title="Delete Instrument Confirmation", message=msg)
        if response:
            return True
        return False

    def _validate_inputs(self, instrument_id, instrument_type):
        """ Validate inputs for id and type """
        if not instrument_id:
            raise ValueError("Instrument_id cannot be empty")
        if not instrument_type or instrument_type not in ['violin', 'piano']:
            raise ValueError("Invalid instrument type")
        try:
            int(instrument_id)
        except:
            raise ValueError("ID must be an integer")