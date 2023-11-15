import customtkinter as ctk 
from tkcalendar import Calendar
from datetime import datetime
from os import path
import sqlite3
from dataclasses import dataclass
from interfaces import Scrollable, Button, Event, EventNameFrames, Entry, Label

@dataclass
class WriteEvent(Event):
    def __post_init__(self):
        Event.__post_init__(self)
        
    def widgets(self):
        Event.widgets(self)
        self.event_label.configure(text = "Escribir datos del evento")
        
        self.name_label = Label(master = self, text = "Nombre del usuario", text_color = "black", font = self.font, 
                                relx = 0.075, rely = 0.17, relwidth = 0.8, relheight = 0.1)
        
        self.name_entry = Entry(master = self, relx = 0.075, rely = 0.27, relwidth = 0.85, relheight = 0.08, placeholder_text = "Nombre del usuario")
        self.name_entry.bind("<Return>", lambda event: self.office_entry.focus_set())
        
        self.office_label = Label(master = self, text = "Bufete", text_color = "black", font = self.font, 
                                relx = 0.075, rely = 0.37, relwidth = 0.8, relheight = 0.1)
        
        self.office_entry = Entry(master = self, relx = 0.075, rely = 0.47, relwidth = 0.85, relheight = 0.08, placeholder_text = "Bufete")
        self.office_entry.bind("<Return>", lambda event: self.position_entry.focus_set())
        
        self.position_label = Label(master = self, text = "Cargo", text_color = "black", font = self.font, 
                                relx = 0.075, rely = 0.57, relwidth = 0.8, relheight = 0.1)
        
        self.position_entry = Entry(master = self, relx = 0.075, rely = 0.67, relwidth = 0.85, relheight = 0.08, placeholder_text = "Cargo")
        self.position_entry.bind("<Return>", lambda event: self.jump_to_name_and_save())
        
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.2, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
        
        self.save_button = Button(master = self, text = "Abrir", relx = 0.55, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.save)
        
    def jump_to_name_and_save(self):
        self.name_entry.delete(0, "end")
        self.office_entry.delete(0, "end")
        self.position_entry.delete(0, "end")
        self.name_entry.focus_set()
                  
@dataclass
class RecorverEvent(Event):
    def __post_init__(self):
        Event.__post_init__(self)
        
    def widgets(self):
        Event.widgets(self)
        self.event_label.configure(text = "Recuperar evento")
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.4, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
        
        self.recorver_scrollframe = Scrollable(master = self, relx = 0.075, rely = 0.2, relwidth = 0.85, relheight = 0.6)
        
        self.search = Entry(master = self, relx = 0.5, rely = 0.07, relwidth = 0.43, relheight = 0.07, placeholder_text = "Buscar")
        
        self._insert_frames(self._extract_data())
        
    def _extract_data(self):
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = cursor.fetchall()
        
        conn.commit()
        conn.close()
        return data
        
    def _insert_frames(self, tables):
        for table in tables:
            frame = EventNameFrames(self.recorver_scrollframe, name = table[0][:-8], date = table[0][-8:])
        
@dataclass
class CalendarEvent(Event):
    def __post_init__(self):
        Event.__post_init__(self)    
        
    def widgets(self):
        Event.widgets(self)         
        self.date = datetime.now().date()

        self.calendar = Calendar(self, selectmode = "day", year = self.date.year, month = self.date.month, day = self.date.day,
                                 background = "#860505", date_pattern = "dd-mm-y")
        self.calendar.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight = 0.99)
        
        self.calendar.calevent_create(self.date, "Hoy", tags="Today")
        self.calendar.tag_config("Today", background = "#860505")
        
        self.calendar.bind("<<CalendarSelected>>", lambda event : self.change_date())
        
    def change_date(self):
        self.master.new_panel_frame.date_button.configure(text = self.calendar.get_date())
        self.animate()

        
        
        

        
        