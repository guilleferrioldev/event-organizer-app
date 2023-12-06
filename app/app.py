import customtkinter as ctk 
import sqlite3
from dataclasses import dataclass 
from new_event import NewEvent
from interfaces import singleton, Label, Scrollable, Entry, Menu, Button, FrameToRegister
from events import WriteEvent, RecorverEvent, CalendarEvent, Confirmation
import pickle
import os
import pandas as pd
from typing import List

@singleton
class App(ctk.CTk):
    """Created app"""
    def __init__(self) -> None:
        ctk.CTk.__init__(self)
        
        # Create application layout
        self.layout()
        
        # Create application layout
        self.widgets()
        
        # Create database 
        self._create_database()
        
        # Visualize
        self.mainloop()
        
    def layout(self) -> None:
        """Custom the app"""
        ctk.set_appearance_mode("light")
        self.title("GEVENT")
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}") 
        self.minsize(self.width,self.height)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.resizable(False, False)

    def widgets(self) -> None:
        """Create widgets to interact with the app"""
        # Fonts
        self.very_small_font = ctk.CTkFont("Arial", 15)
        self.small_font = ctk.CTkFont("Arial", 20, "bold")
        self.big_font = ctk.CTkFont("Arial", 30, "bold")
        self.database = ""
        
        # Visualize the app name
        self.name_app = Label(master = self, text = "GEVENT", text_color = "#860505", font = self.big_font, 
                             relx = 0.05, rely = 0.01, relwidth = 0.2, relheight = 0.1)
        
        self.event_name = Label(master = self, text = "Evento: ", text_color = "#860505", font = self.small_font, 
                             relx = 0.05, rely = 0.085, relwidth = 0.8, relheight = 0.05)
        
        self.count_list = Label(master = self, text = "Cantidad:   0", text_color = "#77767b", font = self.very_small_font,
                                relx = 0.385, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.list_to_register_label = Label(master = self, text = "Listado", text_color = "#77767b", font = self.small_font,
                                            relx = 0.05, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.count_registered_list = Label(master = self, text = "Cantidad:   0", text_color = "#77767b", font = self.very_small_font,
                                            relx = 0.87, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.list_already_register_label = Label(master = self, text = "Acreditados", text_color = "#77767b", font = self.small_font,
                                                relx = 0.53, rely = 0.13, relwidth = 0.15, relheight = 0.03)
        
        self.to_register = Scrollable(master = self, relx = 0.05, rely = 0.23, relwidth = 0.42, relheight = 0.7)
        
        self.already_registered = Scrollable(master = self, relx = 0.53, rely = 0.23, relwidth = 0.42, relheight = 0.7)
        
        self.search_to_register = Entry(master = self, relx = 0.05, rely = 0.17, relwidth = 0.25, relheight = 0.04, 
                                        placeholder_text = "Buscar", state = "disabled")
        self.search_to_register.bind("<KeyRelease>", lambda event: self.search_in_the_list("to register"))
        
        self.search_already_registered = Entry(master = self, relx = 0.53, rely = 0.17, relwidth = 0.25, relheight = 0.04,
                                               placeholder_text = "Buscar", state = "disabled")
        self.search_already_registered.bind("<KeyRelease>", lambda event: self.search_in_the_list("search already registered"))
        
        self.menu_to_register = Menu(master = self, values = [""], relx = 0.31, rely = 0.17, relwidth = 0.16, 
                                     relheight = 0.04, command = self.fitering_by_office_in_list)
        
        self.menu_already_registered = Menu(master = self, values = [""], relx = 0.79, rely = 0.17, relwidth = 0.16,
                                            relheight = 0.04, command = self.fitering_by_office_in_registered_list)
        
        self.new_panel_frame = NewEvent(self)
        self.recorver_event = RecorverEvent(self)
        self.calendar_event_frame = CalendarEvent(self)
        self.write_event = WriteEvent(self)
        self.confirmation_of_export_from_excel = Confirmation(self, text = "Excel extraido", relx_for_confirmation_messages = 0.28)
        
        self.new_event_button = Button(master = self, text = "Nuevo Evento", relx = 0.85,
                                       rely = 0.04, relwidth = 0.1, relheight = 0.05, command = self.animate_new_panel)
        
        self.extract_button = Button(master = self, text = "Extraer excel", relx = 0.74, state = "disabled",
                                       rely = 0.04, relwidth = 0.1, relheight = 0.05, command = self.extract_data_to_excel)
        
    def animate_new_panel(self) -> None:
        """Method to animate the new panel"""
        self.new_panel_frame.animate()
        self.new_panel_frame.name_entry.focus_set()
    
    def _create_database(self) -> None:
        """Create the database when the app is initialized for the first time"""
        conn  = sqlite3.connect("events.db")
        conn.commit()
        conn.close()
        
    def _extract_data(self, name: str) -> List:
        """Method to extract the data from the database"""
        instruction = f"SELECT * FROM {name}"
        data = self.query(instruction)
        return data
    
    def query(self, instruction: str) -> List:
        """Method to make queries with sqlite3"""
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        cursor.execute(instruction)
        
        if instruction.startswith("SELECT"):
            data = cursor.fetchall()
        else:
            data = None
            
        conn.commit()
        conn.close()
        return data
    
    def reset_list(self) -> None:
        """Method to delete all elements from the list"""
        for child in self.to_register.winfo_children():
            child.destroy()
            
    def reset_registerd_list(self) -> None:
        """Method to delete all elements from already registered list"""
        for child in self.already_registered.winfo_children():
            child.destroy()
            
    def insert_data(self, data: List, scrollable: Scrollable) -> None:
        """Method to insert frames in both scrollables list"""
        FrameToRegister(master = scrollable, name = data[0], office = data[1], accredited = data[2], database = self.database)   

    def current_database_of_accredited(self, database: str) -> None:
        """Method to extract data and change the current database"""
        self.database = database
        data = self._extract_data(database)
        
        self.reset_list()
        self.reset_registerd_list()
        self.clean_and_enable_widgets()
        
        for row in data:
            if row[2] == "no":
                self.insert_data(data = row, scrollable = self.to_register)
            else:
                self.insert_data(data = row, scrollable = self.already_registered)
        
        self.insert_values_in_menu()
        self.counter()
        
    def clean_and_enable_widgets(self) -> None:
        """Method to clean and enable widgets"""
        self.search_to_register.delete(0, "end")
        self.search_already_registered.delete(0, "end")
        self.search_to_register.configure(state = "normal")
        self.search_already_registered.configure(state = "normal")
        self.menu_to_register.configure(state = "normal")
        self.menu_already_registered.configure(state = "normal")
            
    def insert_values_in_menu(self) -> None:
        """Method to insert the values in both menus"""
        instruction = f"SELECT * FROM {self.database} WHERE Acreditado = 'no'"
        values = list(set(i[1] for i in self.query(instruction))) + ["Todos"]
        self.menu_to_register.configure(values = values)
        self.menu_to_register.set("Todos")
                
        instruction = f"SELECT * FROM {self.database} WHERE Acreditado = 'yes'"
        values = list(set(i[1] for i in self.query(instruction))) + ["Todos"]
        self.menu_already_registered.configure(values = values)
        self.menu_already_registered.set("Todos")

    def counter(self) -> None:
        """Method to change the state of both counter labels and display the result"""
        self.count_list.configure(text = f"Cantidad: {len([i for i in self.to_register.winfo_children()])}")
        self.count_registered_list.configure(text = f"Cantidad: {len([i for i in self.already_registered.winfo_children()])}")
           
    def execute_instruction(self, instruction: str, scrollable: Scrollable) -> None:
        """Method to excecute instructions, make queries and insert data"""
        data = self.query(instruction)
        
        for row in data:
            self.insert_data(data = row, scrollable = scrollable)
            
        self.counter()
    
    def search_in_the_list(self, scrollable: Scrollable) -> str:
        """Method to search and filter data in both scrollable lists"""
        if scrollable == "to register":
            name = self.search_to_register.get()
            accredited = "no"
            scrollable = self.to_register
            self.reset_list()
        else:
            name = self.search_already_registered.get()
            accredited = "yes"
            scrollable = self.already_registered
            self.reset_registerd_list()
        
        instruction = f"SELECT * FROM {self.database} WHERE Nombre like '%{name}%' AND Acreditado = '{accredited}'"  
        
        if accredited == "no" and self.menu_to_register.get() != "Todos":
            instruction += f" AND Bufete='{self.menu_to_register.get()}'"
        
        if accredited == "yes" and self.menu_already_registered.get() != "Todos":
            instruction += f" AND Bufete='{self.menu_already_registered.get()}'"
            
        self.execute_instruction(instruction, scrollable = scrollable)
            
    def fitering_by_office_in_list(self, choice: str) -> None:
        """Method to filter data in the list when the menu is touched"""
        self.reset_list()
        instruction = f"SELECT * FROM {self.database} WHERE Bufete='{choice}' AND Acreditado='no'"
        
        if choice == "Todos":
            instruction = f"SELECT * FROM {self.database} WHERE Acreditado='no'"
            
        if self.search_to_register.get():
            instruction += f" AND Nombre like '%{self.search_to_register.get()}%'"
        
        self.execute_instruction(instruction, scrollable = self.to_register)
        
    def fitering_by_office_in_registered_list(self, choice: str) -> None:
        """Method to filter data in the already registered list when the menu is touched"""
        self.reset_registerd_list()
        instruction = f"SELECT * FROM {self.database} WHERE Bufete='{choice}' AND Acreditado='yes'"
        
        if choice == "Todos":
            instruction = f"SELECT * FROM {self.database} WHERE Acreditado='yes'"
        
        if self.search_already_registered.get():
            instruction += f" AND Nombre like '%{self.search_already_registered.get()}%'"
        
        self.execute_instruction(instruction, scrollable = self.already_registered)
        
    def extract_data_to_excel(self):
        data = pd.DataFrame(self._extract_data(self.database))
        data.columns = ["Nombre y Apellidos", "Bufete/Categoría", "Acreditado"] 
        path = os.path.expanduser('~/Documents')
        data.to_excel(f"{os.path.join(path, self.database[:-8])}.xlsx", index=False)
        self.confirmation_of_export_from_excel.animate()
        
if __name__ == "__main__": 
    App()