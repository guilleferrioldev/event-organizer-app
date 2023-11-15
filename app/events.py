import customtkinter as ctk 
from tkcalendar import Calendar
from datetime import datetime
from os import path
import sqlite3
from dataclasses import dataclass
from interfaces import Scrollable, Button, Event, EventNameFrames, Entry, Label
from collections import defaultdict

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
        
        self.search = Entry(master = self, relx = 0.5, rely = 0.07, relwidth = 0.35, relheight = 0.07, placeholder_text = "Buscar")
        instruction = f"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name and name like '%{self.search}%'"
        self.search.bind("<KeyRelease>", lambda event: self.searching())
        
        self.sort_button = Button(master = self, text = "N", relx = 0.86, rely = 0.07,
                                  relwidth = 0.07, relheight = 0.07, command = self.sorting)
        
        self.order = True
        self._insert_frames(self._extract_data())
        
    def _extract_data(self, instruction = f"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        cursor.execute(instruction)
        data = cursor.fetchall()
        
        conn.commit()
        conn.close()
        return (i[0] for i in data)
        
    def _insert_frames(self, tables):
        for table in tables:
            EventNameFrames(self.recorver_scrollframe, name = table[:-8], date = table[-8:])
            
    def sorting(self):
        for child in self.recorver_scrollframe.winfo_children():
            child.destroy()
        
        if self.order:
            self.order = False
            self.sort_button.configure(text = "F")
            self._insert_frames(self._order_by_date())
        else:
            self.order = True
            self.sort_button.configure(text = "N")
            self._insert_frames(self._extract_data())
            
    def _order_by_date(self):
        hashmap = defaultdict(list)
        
        names = self._extract_data()
        
        for name in names:
            hashmap[name[-8:]].append(name) 
        
        result = {datetime.strptime(date[:2] + "-" + date[2:4] + "-" + date[4:], '%d-%m-%Y').date(): names for date, names in hashmap.items()}
    
        return sum({key: result[key] for key in sorted(result)}.values(), start = [])
    
    def searching(self):
        for child in self.recorver_scrollframe.winfo_children():
            child.destroy()
            
        instruction = f"SELECT name FROM sqlite_master WHERE type='table' AND name like '%{self.search.get()}%'"
        self._insert_frames(self._extract_data(instruction))
        
@dataclass
class CalendarEvent(Event):
    def __post_init__(self):
        Event.__post_init__(self)    
        
    def widgets(self):
        Event.widgets(self)         
        self.today = datetime.now().date()

        self.calendar = Calendar(self, selectmode = "day", year = self.today.year, month = self.today.month, day = self.today.day,
                                 background = "#860505", date_pattern = "dd-mm-yyyy")
        self.calendar.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight = 0.99)
        
        self.calendar.calevent_create(self.today, "Hoy", tags="Today")
        self.calendar.tag_config("Today", background = "#860505")
        
        self.calendar.bind("<<CalendarSelected>>", lambda event : self.change_date())
        
    def change_date(self):
        if datetime.strptime(self.calendar.get_date(), '%d-%m-%Y').date() >= self.today:
            self.master.new_panel_frame.date_button.configure(text = self.calendar.get_date())
            self.master.new_panel_frame.date = self.calendar.get_date()
            self.animate()
        
        
        

        
        