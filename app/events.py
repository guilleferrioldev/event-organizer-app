import customtkinter as ctk 
from tkcalendar import Calendar
from datetime import datetime
import sqlite3
from dataclasses import dataclass
from interfaces import Scrollable, Button, Event, EventNameFrames, Entry, Label
from collections import defaultdict
from typing import Iterable, List

####################
# WRITE FRAME
####################

@dataclass
class WriteEvent(Event):
    """Frame where names are written by hand"""
    def __post_init__(self) -> None:
        Event.__post_init__(self)
        
    def widgets(self) -> None:
        """Method to insert all widgets"""
        Event.widgets(self)
        self.event_label.configure(text = "Escribir datos del evento")
        
        self.name_label = Label(master = self, text = "Nombre del usuario", text_color = "black", font = self.font, 
                                relx = 0.075, rely = 0.27, relwidth = 0.8, relheight = 0.1)
        
        self.name_entry = Entry(master = self, relx = 0.075, rely = 0.37, relwidth = 0.85, relheight = 0.08, 
                                placeholder_text = "Insertar nombre del usuario")
        self.name_entry.bind("<Return>", lambda event: self.office_entry.focus_set())
        
        self.office_label = Label(master = self, text = "Bufete/Invitado", text_color = "black", font = self.font, 
                                relx = 0.075, rely = 0.5, relwidth = 0.8, relheight = 0.1)
        
        self.office_entry = Entry(master = self, relx = 0.075, rely = 0.6, relwidth = 0.85, relheight = 0.08,
                                  placeholder_text = "Insertar Bufete")
        self.office_entry.bind("<Return>", lambda event: self.jump_to_name_and_save())
        
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.2, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
        
        self.save_button = Button(master = self, text = "Abrir", relx = 0.55, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.save)
        
    def get_database_name(self) -> str:
        """Method to get database name"""
        return "_".join(self.master.new_panel_frame.name_entry.get().split()).title() + "".join(self.master.new_panel_frame.date.split("-"))
    
        
    def jump_to_name_and_save(self) -> None:
        """Method to save the data and jump to name_entry"""
        if not (self.name_entry.get() and self.office_entry.get()):
            self.verification_message(valid = False)
            return
         
        name = self.name_entry.get().title()
        office = self.office_entry.get().title()
        accredited = "no"
        
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        data_insert = f"""INSERT INTO {self.get_database_name()} 
                        (Nombre,
                        Bufete,
                        Acreditado)
                        VALUES (?,?,?)"""
                            
        data_insert_tuple = (name, office, accredited)
        
        cursor.execute(data_insert, data_insert_tuple)
        conn.commit()
        conn.close()
        
        self.clean_entries()
        self.verification_message(valid = True)
        self.name_entry.focus_set()
        
    def verification_message(self, valid: bool) -> None:
        """Method to validate if the name was written"""
        if not valid:
            self.name_entry.configure(placeholder_text = "¡Debe insertar el nombre del usuario!", placeholder_text_color = "red")
            self.office_entry.configure(placeholder_text = "¡Debe insertar si el usuario es de un bufete o invitado!", placeholder_text_color = "red")
        else:
            self.name_entry.configure(placeholder_text = "Insertar nombre del usuario", placeholder_text_color = "grey")
            self.office_entry.configure(placeholder_text = "Bufete/Invitado", placeholder_text_color = "grey")
    
    def clean_entries(self) -> None:
        """Method to clean entries"""
        self.name_entry.delete(0, "end")
        self.office_entry.delete(0, "end")
        
    def cancel(self) -> None:
        """Cancel method"""
        Event.cancel(self)
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        instruccion = f"DROP TABLE IF EXISTS {self.get_database_name()};"
        cursor.execute(instruccion)
        
        conn.commit()
        conn.close()
        
        self.clean_entries()
    
    def save(self) -> None:
        """Method to save the data and open it"""
        self.master.event_name.configure(text = f"Evento: {' '.join(self.get_database_name()[:-8].split('_'))}")
        self.clean_entries()
        self.master.current_database_of_accredited(self.get_database_name())
        self.master.recorver_event.refresh()
        self.master.new_panel_frame.cancel()
        self.master.extract_button.configure(state = "normal")
        self.animate() 
 
 
####################
# RECORVER FRAME
####################                 
@dataclass
class RecorverEvent(Event):
    """Frame to recorver the data"""
    def __post_init__(self) -> None:
        Event.__post_init__(self)
        
    def widgets(self) -> None:
        """Method to insert all widgets"""
        Event.widgets(self)
        self.event_label.configure(text = "Recuperar evento")
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.4, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
        
        self.recorver_scrollframe = Scrollable(master = self, relx = 0.075, rely = 0.2, relwidth = 0.85, relheight = 0.6)
        
        self.search = Entry(master = self, relx = 0.5, rely = 0.07, relwidth = 0.35, relheight = 0.07, placeholder_text = "Buscar")
        self.search.bind("<KeyRelease>", lambda event: self.searching())
        
        self.sort_button = Button(master = self, text = "F", relx = 0.86, rely = 0.07,
                                  relwidth = 0.07, relheight = 0.07, command = self.sorting)
        
        self.order = True
        self._insert_frames(self._extract_data())
        
    def _extract_data(self, instruction: str = f"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name") -> Iterable:
        """Method to extract the data from the database"""
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        cursor.execute(instruction)
        data = cursor.fetchall()
        
        conn.commit()
        conn.close()
        return (i[0] for i in data)
        
    def _insert_frames(self, tables: List) -> None:
        """Method to insert data in scrollable list"""
        for table in tables:
            EventNameFrames(self.recorver_scrollframe, table_name = table)
            
    def sorting(self) -> None:
        """Method to sort data"""
        for child in self.recorver_scrollframe.winfo_children():
            child.destroy()
        
        if self.order:
            self.order = False
            self.sort_button.configure(text = "N")
            self._insert_frames(self._order_by_date())
        else:
            self.order = True
            self.sort_button.configure(text = "F")
            self._insert_frames(self._extract_data())
            
    def _order_by_date(self) -> List:
        """Method to sort data according to date"""
        hashmap = defaultdict(list)
    
        names = self._extract_data()
        
        for name in names:
            hashmap[name[-8:]].append(name) 
        
        result = {datetime.strptime(date[:2] + "-" + date[2:4] + "-" + date[4:], '%d-%m-%Y').date(): names for date, names in hashmap.items()}
    
        return sum({key: result[key] for key in sorted(result)}.values(), start = [])
    
    def searching(self) -> None:
        """Method to search when you type in the search entry"""
        for child in self.recorver_scrollframe.winfo_children():
            child.destroy()
            
        if len(self.search.get()) == 0:
            self.order = False
            self.sorting()
            return
            
        instruction = f"SELECT name FROM sqlite_master WHERE type='table' AND name like '%{self.search.get()}%'"
        self._insert_frames(self._extract_data(instruction))
    
    def refresh(self) -> None:
        """Method to refresh this frames"""
        self.order = False
        self.sorting()
        
    def cancel(self) -> None:
        """Method to cancel"""
        Event.cancel(self)
        self.search.delete(0, "end")
        self.search.configure(placeholder_text = "Buscar")
        self.master.extract_button.configure(state = "normal")
        self.refresh()
        
        
####################
# CALENDAR FRAME
####################    
@dataclass
class CalendarEvent(Event):
    """Frame to change the date"""
    def __post_init__(self) -> None:
        Event.__post_init__(self)    
        
    def widgets(self) -> None:
        """Method to insert all widgets"""
        Event.widgets(self)         
        self.today = datetime.now().date()

        self.calendar = Calendar(self, selectmode = "day", year = self.today.year, month = self.today.month, day = self.today.day,
                                 background = "#860505", date_pattern = "dd-mm-yyyy")
        self.calendar.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight = 0.99)
        
        self.calendar.calevent_create(self.today, "Hoy", tags="Today")
        self.calendar.tag_config("Today", background = "#860505")
        
        self.calendar.bind("<<CalendarSelected>>", lambda event : self.change_date())
        
    def change_date(self) -> None:
        """Method to change the date"""
        if datetime.strptime(self.calendar.get_date(), '%d-%m-%Y').date() >= self.today:
            self.master.new_panel_frame.date_button.configure(text = self.calendar.get_date())
            self.master.new_panel_frame.date = self.calendar.get_date()
            self.animate()
        
########################
# CONFIRMATION FRAME
#######################       
@dataclass
class Confirmation(Event):
    """Frame to get confirmation"""
    def __post_init__(self) -> None:
        Event.__post_init__(self)       
        
    def widgets(self) -> None:
        """Method to insert all widgets"""
        Event.widgets(self)    
        self.font = ctk.CTkFont("Arial", 30, "bold")
        
        self.message = Label(master = self, text = "Excel extraido", text_color = "#860505", font = self.font, 
            relx = 0.28, rely = 0.2, relwidth = 0.8, relheight = 0.5)
        
        self.ok_button = Button(master = self, text = "OK", relx = 0.4, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.animate)
        
        