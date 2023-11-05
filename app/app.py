import customtkinter as ctk 
import sqlite3
from os import path
from dataclasses import dataclass 
from interfaces import Label, Scrollable, Entry, Menu, Button, InterfaceSlidingFrame, ImageButton, FrameToRegister

def singleton(cls):
    """Decorator to only have one application open"""
    __instance = dict()

    def wrapper(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
        return __instance[cls]
    return  wrapper

@singleton
class App(ctk.CTk):
    """Created app"""
    def __init__(self):
        ctk.CTk.__init__(self)
        
        # Create application layout
        self.create_layout()
        
        # Create application layout
        self.create_widgets()
        
        # Visualize
        self.mainloop()
        
    def create_layout(self):
        ctk.set_appearance_mode("light")
        self.title("GEVENT")
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}") 
        #self.geometry("1920x1080") 
        self.minsize(self.width,self.height)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.resizable(True, True)

    def create_widgets(self):
        # Fonts
        self.small_font = ctk.CTkFont("Arial", 20, "bold")
        self.big_font = ctk.CTkFont("Arial", 30, "bold")
        
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
        
        self.search_to_register = Entry(master = self, relx = 0.05, rely = 0.17, relwidth = 0.25, relheight = 0.04)
        
        self.search_already_registered = Entry(master = self, relx = 0.53, rely = 0.17, relwidth = 0.25, relheight = 0.04)
        
        self.menu_to_register = Menu(master = self, values = [""], relx = 0.31, rely = 0.17, relwidth = 0.16, relheight = 0.04)
        
        self.menu_already_registered = Menu(master = self, values = [""], relx = 0.79, rely = 0.17, relwidth = 0.16, relheight = 0.04)
        
        self.frame = FrameToRegister(self.to_register, name = "Jose antonio alvarez echecherria cuadrado", office = "Bufete", position = "Cargo")
        
        self.new_panel_frame = NewEvent(self, 1.0, 0.7)
        
        self.new_event_button = Button(master = self, text = "Nuevo Evento", relx = 0.85,
                                       rely = 0.04, relwidth = 0.1, relheight = 0.05, command = self.new_panel_frame.animate)
    
    
@dataclass
class NewEvent(InterfaceSlidingFrame):
    def __post_init__(self):
        InterfaceSlidingFrame.__post_init__(self)
        
    def widgets(self):
        self.name_label = Label(master = self, text = "Nombre del evento", text_color = "#860505", font = self.font, 
                                relx = 0.075, rely = 0.05, relwidth = 0.4, relheight = 0.1)
        
        self.name_entry = Entry(master = self, relx = 0.075, rely = 0.14, relwidth = 0.85, relheight = 0.08)
        
        self.write_label = Label(master = self, text = "Escribir", text_color = "#860505", font = self.font, 
                               relx = 0.14, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.excel_label = Label(master = self, text = "Excel", text_color = "#860505", font = self.font, 
                                relx = 0.46, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.trash_label = Label(master = self, text = "Recuperar", text_color = "#860505", font = self.font, 
                                relx = 0.72, rely = 0.25, relwidth = 0.4, relheight = 0.1)
        
        self.write = ImageButton(master = self, path = path.join(".", "pngs", "write.png"), relx = 0.075, rely = 0.34, relwidth = 0.25, relheight = 0.45)
        
        self.excel = ImageButton(master = self, path = path.join(".", "pngs", "excel.png"), relx = 0.375, rely = 0.34, relwidth = 0.25, relheight = 0.45)
        
        self.trash = ImageButton(master = self, path = path.join(".", "pngs", "trash.png"), relx = 0.675, rely = 0.34, relwidth = 0.25, relheight = 0.45)
        
        self.cancel_button = Button(master = self, text = "Cancelar", relx = 0.4, rely = 0.85,
                                  relwidth = 0.2, relheight = 0.1, command = self.cancel)
        
    def cancel(self):
        self.name_entry.delete(0, "end")
        self.animate()
    
    def create_database(self, name = "new"):
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        table = f""" CREATE TABLE IF NOT EXISTS {name}
                    (Nombre y Apellidos TEXT,
                    Bufete TEXT,
                    Cargo TEXT,
                    Acreditado Text)
        """
        conn.execute(table)
        
        conn.commit()
        conn.close()
        
        
App()