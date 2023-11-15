import customtkinter as ctk 
from datetime import datetime
from os import path
import sqlite3
from dataclasses import dataclass
from interfaces import Label, Entry, InterfaceSlidingFrame, ImageButton, Button
from events import WriteEvent, RecorverEvent, CalendarEvent

@dataclass
class NewEvent(InterfaceSlidingFrame):
    def __post_init__(self):
        InterfaceSlidingFrame.__post_init__(self)
        
    def widgets(self):
        self.name_label = Label(master = self, text = "Nombre del evento", text_color = "#860505", font = self.font, 
                                relx = 0.075, rely = 0.05, relwidth = 0.4, relheight = 0.1)
        
        self.name_entry = Entry(master = self, relx = 0.075, rely = 0.14, relwidth = 0.67, relheight = 0.08, placeholder_text = "Nombre del evento")
        self.name_entry.bind("<Return>", lambda event: self.focus_set())
        self.name_entry.bind("<KeyRelease>", lambda event: self.change_entry_focus())
        self.after(10000, lambda: self.focus_set())
        
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
    
    def change_date(self):
        self.focus_set()
        self.calendar_event_frame = CalendarEvent(self.master).animate()
        
    def change_entry_focus(self):
        self.after(10000, lambda: self.focus_set())
        
    def cancel(self):
        self.name_entry.delete(0, "end")
        self.date = self.today
        self.date_button.configure(text = f"{self.today}")
        self.animate()
    
    def write_data(self):
        self.focus_set()
        if self.name_entry.get():
            self.create_database()
            self.write_event = WriteEvent(self.master).animate()
        else:
            self.name_entry.configure(placeholder_text = "¡Debe insertar el nombre del evento!", placeholder_text_color = "red")
        
    def import_data_from_excel(self):
        self.focus_set()
        if self.name_entry.get():
            print("si")
        else:
            self.name_entry.configure(placeholder_text = "¡Debe insertar el nombre del evento!", placeholder_text_color = "red")
    
    def recorver_data(self):
        self.focus_set()
        self.name_entry.configure(placeholder_text = "Nombre del evento", placeholder_text_color = "grey")
        self.recorver_event = RecorverEvent(self.master).animate()
    
    def create_database(self):
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        name = "_".join(self.name_entry.get().split()) + "".join(self.date.split("-"))
        table = f""" CREATE TABLE IF NOT EXISTS {name}
                    (Nombre y Apellidos TEXT,
                    Bufete TEXT,
                    Cargo TEXT,
                    Acreditado Text)
        ;"""
        cursor.execute(table)

        conn.commit()
        conn.close()
        

        