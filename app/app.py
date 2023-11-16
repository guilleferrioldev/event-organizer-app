import customtkinter as ctk 
import sqlite3
from os import path
from dataclasses import dataclass 
from new_event import NewEvent
from interfaces import singleton, Label, Scrollable, Entry, Menu, Button, FrameToRegister
from events import WriteEvent, RecorverEvent, CalendarEvent

@singleton
class App(ctk.CTk):
    """Created app"""
    def __init__(self):
        ctk.CTk.__init__(self)
        
        # Create application layout
        self.layout()
        
        # Create application layout
        self.widgets()
        
        # Create database 
        self._create_database()
        
        # Visualize
        self.mainloop()
        
    def layout(self):
        """Custom the app"""
        ctk.set_appearance_mode("light")
        self.title("GEVENT")
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}") 
        self.minsize(self.width,self.height)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.resizable(False, False)

    def widgets(self):
        """Create widgets to interact with the app"""
        # Fonts
        self.small_font = ctk.CTkFont("Arial", 20, "bold")
        self.big_font = ctk.CTkFont("Arial", 30, "bold")
        self.database = ""
        
        # Visualize the app name
        self.name_app = Label(master = self, text = "GEVENT", text_color = "#860505", font = self.big_font, 
                             relx = 0.05, rely = 0.01, relwidth = 0.2, relheight = 0.1)
        
        self.event_name = Label(master = self, text = "Evento: ", text_color = "#860505", font = self.small_font, 
                             relx = 0.05, rely = 0.09, relwidth = 0.2, relheight = 0.03)
        
        self.list_to_register_label = Label(master = self, text = "Listado", text_color = "#77767b", font = self.small_font,
                                            relx = 0.05, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.list_already_register_label = Label(master = self, text = "Acreditados", text_color = "#77767b", font = self.small_font,
                                                relx = 0.53, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.to_register = Scrollable(master = self, relx = 0.05, rely = 0.23, relwidth = 0.42, relheight = 0.7)
        
        self.already_registered = Scrollable(master = self, relx = 0.53, rely = 0.23, relwidth = 0.42, relheight = 0.7)
        
        self.search_to_register = Entry(master = self, relx = 0.05, rely = 0.17, relwidth = 0.25, relheight = 0.04, placeholder_text = "Buscar")
        
        self.search_already_registered = Entry(master = self, relx = 0.53, rely = 0.17, relwidth = 0.25, relheight = 0.04, placeholder_text = "Buscar")
        
        self.menu_to_register = Menu(master = self, values = [""], relx = 0.31, rely = 0.17, relwidth = 0.16, relheight = 0.04)
        
        self.menu_already_registered = Menu(master = self, values = [""], relx = 0.79, rely = 0.17, relwidth = 0.16, relheight = 0.04)
        
        self.new_panel_frame = NewEvent(self)
        self.recorver_event = RecorverEvent(self)
        self.calendar_event_frame = CalendarEvent(self)
        self.write_event = WriteEvent(self)
        
        self.new_event_button = Button(master = self, text = "Nuevo Evento", relx = 0.85,
                                       rely = 0.04, relwidth = 0.1, relheight = 0.05, command = self.animate_new_panel)

    def animate_new_panel(self):
        self.new_panel_frame.animate()
        self.new_panel_frame.name_entry.focus_set()
    
    def _create_database(self):
        """Create the database when the app is initialized for the first time"""
        conn  = sqlite3.connect("events.db")
        conn.commit()
        conn.close()
        
    def _extract_data(self, name):
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        instruction = f"SELECT * FROM {name}"
        cursor.execute(instruction)
        data = cursor.fetchall()

        conn.commit()
        conn.close()
        return data

    def current_database_of_accredited(self, database):
        self.database = database
        data = self._extract_data(database)
        
        for child in self.to_register.winfo_children():
            child.destroy()
            
        for child in self.already_registered.winfo_children():
            child.destroy()
        
        for row in data:
            if row[3] == "no":
                FrameToRegister(self.to_register, name = row[0], office = row[1], position = row[2], accredited = row[3],  database = database)
            else:
                FrameToRegister(self.already_registered, name = row[0], office = row[1], position = row[2], accredited = row[3], database = database)
        
        values = [row[1] for row in data]
        self.menu_to_register.configure(values = values)
        self.menu_to_register.set(values[0] if values else "")
        self.menu_already_registered.configure(values = values)
        self.menu_already_registered.set(values[0] if values else "")
        
    
if __name__ == "__main__":    
    App()