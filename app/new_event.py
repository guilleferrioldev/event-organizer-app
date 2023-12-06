import customtkinter as ctk 
from datetime import datetime
from os import path
from pathlib import Path
from tkinter import filedialog
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from dataclasses import dataclass
from interfaces import Label, Entry, InterfaceSlidingFrame, ImageButton, Button
from events import WriteEvent, RecorverEvent, CalendarEvent

@dataclass
class NewEvent(InterfaceSlidingFrame):
    def __post_init__(self) -> None:
        InterfaceSlidingFrame.__post_init__(self)
        
    def widgets(self) -> None:
        """Method to insert all widgets"""
        self.name_label = Label(master = self, text = "Nombre del evento", text_color = "#860505", font = self.font, 
                                relx = 0.075, rely = 0.05, relwidth = 0.4, relheight = 0.1)
        
        self.name_entry = Entry(master = self, relx = 0.075, rely = 0.14, relwidth = 0.67, relheight = 0.08, 
                                placeholder_text = "Insertar nombre del evento")
        self.name_entry.bind("<Return>", lambda event: self.focus_set())
        self.name_entry.bind("<KeyRelease>", lambda event: self.change_entry_focus())
        self.after(3000, lambda: self.focus_set())
        
        self.today  = datetime.now().date().strftime("%d-%m-%Y")
        self.date = self.today
        self.date_button = Button(master = self, text = f"{self.today}", relx = 0.76, rely = 0.14,
                                  relwidth = 0.16, relheight = 0.08, command = self.change_date)
        
        self.write_label = Label(master = self, text = "Escribir", text_color = "#860505", font = self.font, 
                               relx = 0.14, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.excel_label = Label(master = self, text = "Excel", text_color = "#860505", font = self.font, 
                                relx = 0.46, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.trash_label = Label(master = self, text = "Recuperar", text_color = "#860505", font = self.font, 
                                relx = 0.72, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.write = ImageButton(master = self, path = path.join(".", "pngs", "write.png"), relx = 0.075,
                                 rely = 0.34, relwidth = 0.25, relheight = 0.45, command = self.write_data)
        
        self.excel = ImageButton(master = self, path = path.join(".", "pngs", "excel.png"), relx = 0.375, 
                                 rely = 0.34, relwidth = 0.25, relheight = 0.45, command = self.import_data_from_excel)
        
        self.trash = ImageButton(master = self, path = path.join(".", "pngs", "trash.png"), relx = 0.675, 
                                 rely = 0.34, relwidth = 0.25, relheight = 0.45, command = self.recorver_data)
        
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.4, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
    
    def change_date(self) -> None:
        """Method to animate the Calendar Event frame"""
        self.focus_set()
        self.master.calendar_event_frame.animate()
        
    def change_entry_focus(self) -> None:
        """Method to remove focus from name_entry"""
        self.after(3000, lambda: self.focus_set())
        
    def cancel(self) -> None:
        """Cancel method"""
        self.name_entry.delete(0, "end")
        self.date = self.today
        self.date_button.configure(text = f"{self.today}")
        self.animate()
    
    def write_data(self) -> None:
        """Method to animate the Write Event frame"""
        self.focus_set()
        if self.name_entry.get():
            self.create_database()
            self.master.write_event.animate()
        else:
            self.name_entry.configure(placeholder_text = "¡Debe insertar el nombre del evento!", placeholder_text_color = "red")
        
    def import_data_from_excel(self) -> None:
        """Method to animate the Excel Event frame"""
        self.focus_set()
        if self.name_entry.get():
            self.import_excel()
        else:
            self.name_entry.configure(placeholder_text = "¡Debe insertar el nombre del evento!", placeholder_text_color = "red")
    
    def recorver_data(self) -> None:
        """Method to animate the Recorver Event frame"""
        self.focus_set()
        self.name_entry.configure(placeholder_text = "Insertar nombre del evento", placeholder_text_color = "grey")
        self.master.recorver_event.animate()
    
    def create_database(self) -> None:
        """Method to create a database when excel button or write button are touched"""
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        name = "_".join(self.name_entry.get().split()) + "".join(self.date.split("-"))
        table = f""" CREATE TABLE IF NOT EXISTS {name}
                    (Nombre TEXT,
                    Bufete TEXT,
                    Acreditado Text)
        ;"""
        cursor.execute(table)

        conn.commit()
        conn.close()  
        
    def import_excel(self) -> None:
        """Method to open the excel"""
        filename = filedialog.askopenfilename(title = "Abrir excel", initialdir = "~")
        if filename:
            path = Path(filename)
            self._path_to_sql(path)
            
    def _path_to_sql(self, path) -> None:
        """Method to insert the excel in the database"""
        if not str(path).endswith(".xlsx") or str(path).endswith(".xls"):
            return 
        
        excel = pd.read_excel(path)
        if excel.shape[1] > 3:
            return
        
        excel.columns = ["Nombre", "Bufete"]
        excel["Acreditado"] = ["no" for i in range(excel.shape[0])]
        
        engine = create_engine('sqlite:///events.db')
        name_of_table = "_".join(self.name_entry.get().split()) + "".join(self.date.split("-"))
        excel.to_sql(name_of_table, con=engine, if_exists='replace', index=False)
        
        self._open(name_of_table)
    
    def _open(self, database) -> None:
        """Method to open the data"""
        self.master.current_database_of_accredited(database)
        self.master.recorver_event.refresh()
        self.cancel()
      
        