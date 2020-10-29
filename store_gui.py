"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    Store gui
"""
import tkinter as tk
import tkinter.font
from tkinter import ttk
import requests
from add_piano_popup import AddPianoPopup
from add_violin_popup import AddViolinPopup
from remove_instrument_popup import RemoveInstrumentPopup
from update_instrument_popup import UpdateInstrumentPopup
from create_tables import create_db_tables
from drop_tables import drop_db_tables

class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        create_db_tables()
        self._url = "http://127.0.0.1:5000/store/instrument/"
        tk.Frame.__init__(self, parent)

        # Left frame, column 1
        left_frame = tk.Frame(master=self)
        left_frame.grid(row=1, column=1)

        # Right frame (info text, column 2)
        right_frame = tk.Frame(master=self)
        right_frame.grid(row=1, column=2)

        # Listbox for people
        tk.Label(left_frame, text="Instruments list:").grid(row=1, column=1, columnspan=3)
        self._instruments_list = tk.Listbox(left_frame, width=20)
        self._instruments_list.grid(row=2, column=1, columnspan=3)
        # Call this on select
        self._instruments_list.bind("<<ListboxSelect>>", self._update_textbox)

        # A couple buttons - using TTK
        ttk.Button(left_frame, text="Pianos", command=self._get_pianos).grid(row=3, column=2)
        ttk.Button(left_frame, text="Violins", command=self._get_violins).grid(row=3, column=3)
        ttk.Button(left_frame, text="Quit", command=self._quit_callback).grid(row=5, column=2, columnspan=2)
        ttk.Button(left_frame, text="Clear database", command=self._clear_database).grid(row=6, column=2, columnspan=2)

        # Right frame widgets
        self._info_text = tk.Text(master=right_frame, height=10, width=40, font=("TkTextFont", 10))
        self._info_text.grid(row=1, column=1, columnspan=2)
        self._info_text.tag_configure("bold", font=("TkTextFont", 10, "bold"))
        ttk.Button(right_frame, text="Add Piano", command=self._add_piano).grid(row=3, column=1)
        ttk.Button(right_frame, text="Add Violin", command=self._add_violin).grid(row=3, column=2)

        ttk.Button(right_frame, text="Update Instrument", command=self._update_instrument).grid(row=4, column=1)
        ttk.Button(right_frame, text="Remove Instrument", command=self._remove_instrument).grid(row=4, column=2)

        # # Now update the list
        self._get_all_instruments()

    def _get_all_instruments(self):
        """ Update the List of Instruments """
        r = requests.get(self._url + "all")
        self._instruments_list.delete(0, tk.END)
        for s in r.json():
            self._instruments_list.insert(tk.END, s['instrument_type'] + ' ' + str(s['id']))
            if s['instrument_type'] == "piano":
                self._instruments_list.itemconfig(tk.END, {'fg': 'blue'})

    def _get_pianos(self):
        """ Update the List of Pianos """
        r = requests.get(self._url + "all/piano")
        self._instruments_list.delete(0, tk.END)
        for s in r.json():
            self._instruments_list.insert(tk.END, s['instrument_type'] + ' ' + str(s['id']))  
            self._instruments_list.itemconfig(tk.END, {'fg': 'blue'})

    def _get_violins(self):
        """ Update the List of Violins """
        r = requests.get(self._url + "all/violin")
        self._instruments_list.delete(0, tk.END)
        for s in r.json():
            self._instruments_list.insert(tk.END, s['instrument_type'] + ' ' + str(s['id']))

    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """

        # This is a list, so we take just the first item (could be multi select...)
        selected_values = self._instruments_list.curselection()
        # if selected_values:
        if selected_values:
            selected_index = selected_values[0]
            instrument_name = self._instruments_list.get(selected_index)

            # Make a GET request
            instrument_name_list = instrument_name.split()
            instrument_type = instrument_name_list[0]
            instrument_id = instrument_name_list[1]
            r = requests.get(self._url + instrument_type + '/' + instrument_id)

            # Clear the text box
            self._info_text.delete(1.0, tk.END)

            # Check the request status code
            if r.status_code != 200:
                self._info_text.insert(tk.END, "Error running the request!")

            for k, v in r.json().items():
                self._info_text.insert(tk.END, f"{k.capitalize()}\t\t\t", "bold")
                self._info_text.insert(tk.END, f"{v}\n")

    def _add_piano(self):
        """ Add Piano Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddPianoPopup(self._popup_win, self._updated_close_cb)

    def _add_violin(self):
        """ Add Violin Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddViolinPopup(self._popup_win, self._updated_close_cb)

    def _close_cb(self):
        """ Close Add Student Popup """
        self._popup_win.destroy()
        self._get_all_instruments()

    def _update_instrument(self):
        """ Update Instrument Popup """
        self._popup_win = tk.Toplevel()
        self._popup = UpdateInstrumentPopup(self._popup_win, self._updated_close_cb)

    def _remove_instrument(self):
        """ Remove Instrument Popup """
        self._popup_win = tk.Toplevel()
        self._popup = RemoveInstrumentPopup(self._popup_win, self._updated_close_cb)

    def _updated_close_cb(self):
        """ Close Add Student Popup """
        self._popup_win.destroy()
        self._get_all_instruments()
        self._info_text.delete(1.0, tk.END)

    def _quit_callback(self):
        """ Quit """
        self.quit()
    
    def _clear_database(self):
        """ Button to clear the database file """
        drop_db_tables()
        create_db_tables()
        self._get_all_instruments()
        self._info_text.delete(1.0, tk.END)

  
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    MainAppController(root).pack()
    root.mainloop()


