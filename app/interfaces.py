import customtkinter as ctk 
from dataclasses import dataclass 
from abc import ABC, abstractmethod
from typing import List, Callable
from PIL import Image
import sqlite3

def singleton(cls):
    """Singleton decorator"""
    __instance = dict()

    def wrapper(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
        return __instance[cls]
    return  wrapper

####################
# LABELS
####################
@dataclass
class InterfaceLabel(ABC, ctk.CTkLabel):
    """Interface to generate labels"""
    master: ctk.CTkFrame
    text: str
    text_color: str
    font: ctk.CTkFont
    relx: float
    rely: float
    relwidth: float
    relheight: float
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkLabel.__init__(self,
                            master = self.master,
                            text = self.text,
                            font = self.font,
                            text_color = self.text_color,
                            anchor = "w")
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
@dataclass
class Label(InterfaceLabel):
    """Class to create concrete labels"""
    def __post_init__(self) ->  None:
        InterfaceLabel.__post_init__(self)   
     
     
        
####################
# SCROLLABLE FRAME
####################       
@dataclass
class InterfaceScrollableFrame(ABC, ctk.CTkScrollableFrame):
    """Interface to generate scrollable frames"""
    master: ctk.CTkFrame
    relx: float
    rely: float
    relwidth: float
    relheight: float
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkScrollableFrame.__init__(self, master = self.master)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
@dataclass
class Scrollable(InterfaceScrollableFrame):
    """Class to create concrete scrollable frame"""
    def __post_init__(self) -> None:
        InterfaceScrollableFrame.__post_init__(self)   


####################
# ENTRY
####################   
@dataclass
class InterfaceEntry(ABC, ctk.CTkEntry):
    """Interface to generate entries"""
    master: ctk.CTkFrame
    relx: float
    rely: float
    relwidth: float
    relheight: float
    placeholder_text : str
    state : str = "normal"
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkEntry.__init__(self, master = self.master, placeholder_text = self.placeholder_text, font = ctk.CTkFont("Arial", 15), state = self.state)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)


@dataclass
class Entry(InterfaceEntry):
    """Class to create concrete entry"""
    def __post_init__(self) -> None:
        InterfaceEntry.__post_init__(self)   
        

####################
# OPTION MENU
####################   
@dataclass
class InterfaceMenu(ABC, ctk.CTkOptionMenu):
    """Interface to generate Option menus"""
    master: ctk.CTkFrame
    values: List[str]
    relx: float
    rely: float
    relwidth: float
    relheight: float
    command: Callable
    state: str = "disabled"
    
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkOptionMenu.__init__(self, master = self.master, values = self.values, fg_color = "#860505", button_color = "red", state = self.state, 
                                   button_hover_color = "#860505", dropdown_hover_color = "red", font = ctk.CTkFont("Arial", 15), command = self.command)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)


@dataclass
class Menu(InterfaceMenu):    
    """Class to create concrete option menu"""
    def __post_init__(self) -> None:
        InterfaceMenu.__post_init__(self)   
        
        
####################
# BUTTON
####################       
@dataclass
class InterfaceButton(ABC, ctk.CTkButton):
    """Interface to generate buttons"""
    master: ctk.CTkFrame
    text: str
    command: Callable
    relx: float
    rely: float
    relwidth: float
    relheight: float
    state: str = "normal"
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkButton.__init__(self, master = self.master, text = self.text, font = ctk.CTkFont("Arial", 12),
                               fg_color= "#860505", hover_color = "red", command = self.command, state = self.state)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
@dataclass
class Button(InterfaceButton):
    """Class to create concrete button"""
    def __post_init__(self) -> None:
        InterfaceButton.__post_init__(self)   
        
  
####################
# IMAGE BUTTON
#################### 
@dataclass
class InterfaceImageButton(ABC, ctk.CTkButton):
    """Interface to generate image buttons"""
    master: ctk.CTkFrame
    path: str
    command: Callable
    relx: float
    rely: float
    relwidth: float
    relheight: float
    
    @abstractmethod
    def __post_init__(self) -> None:
        the_image = ctk.CTkImage(light_image = Image.open(self.path), size = (120, 130))
        ctk.CTkButton.__init__(self, master = self.master,text = "", image = the_image,
                               fg_color = "#860505", hover_color = "red", command = self.command)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
 
@dataclass
class ImageButton(InterfaceImageButton):
    """Class to create concrete image button"""
    def __post_init__(self) -> None:
        InterfaceImageButton.__post_init__(self)   
        
           
####################
# SLIDING FRAME
####################       
@dataclass
class InterfaceSlidingFrame(ABC, ctk.CTkFrame):
    """Interface to generate sliding frames"""
    master: ctk.CTkFrame
    start_pos: float = 1.0
    end_pos: float = 0.7
    text: str = ""
    relx_for_confirmation_messages : float = None
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkFrame.__init__(self, master = self.master, fg_color = "#77767b")
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        self.font = ctk.CTkFont("Arial", 15, "bold")
        self.widgets()
        
        self.place(relx = self.start_pos, rely = 0.25)
        
    @abstractmethod
    def widgets(self) -> None:
        pass
        
    def animate(self) -> None:
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()

    def animate_fordward(self) -> None:
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = 0.25, rely = 0.25, relwidth = 0.45, relheight = 0.5)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self) -> None:
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.25)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

@dataclass
class Event(InterfaceSlidingFrame):
    """Class to create concrete sliding frames"""
    def __post_init__(self) -> None:
        InterfaceSlidingFrame.__post_init__(self)
        
    def widgets(self) -> None:
        self.event_font = ctk.CTkFont("Arial", 20, "bold")
        self.event_label = Label(master = self, text = "", text_color = "#860505", font = self.event_font, 
                                relx = 0.075, rely = 0.05, relwidth = 0.8, relheight = 0.1)
    
    def cancel(self) -> None:
        self.animate()
 
          
####################
# NAME FRAMES
####################
@dataclass
class InterfaceRegisterNameFrames(ABC, ctk.CTkFrame):
    """Interface to generate name frames for scrollable lists in the main window"""
    master: ctk.CTkFrame
    name: str
    office: str
    accredited: str
    database: str
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkFrame.__init__(self, master = self.master, fg_color = "white", height = 100)
        self.widgets()
        
        self.pack(expand = True, fill = "x", padx = 5, pady = 5)
    
    def widgets(self) -> None:
        self.name_font = font = ctk.CTkFont("Arial", 18, "bold")
        self.office_font = font = ctk.CTkFont("Arial", 15)
        
        self.name_label = Label(master = self, text = self.name, text_color = "#860505", font = self.name_font, 
                             relx = 0.05, rely = 0.2, relwidth = 0.8, relheight = 0.3)
        
        self.office_label = Label(master = self, text = f"Bufete/Cat: {self.office}", text_color = "#77767b", font = self.office_font, 
                             relx = 0.05, rely = 0.6, relwidth = 0.8, relheight = 0.2)

@dataclass
class FrameToRegister(InterfaceRegisterNameFrames):
    """Class to create concrete name frames for scrollable lists in the main window"""
    def __post_init__(self) -> None:
        InterfaceRegisterNameFrames.__post_init__(self)  
        self.check = Button(master = self, text = "\u2194", relx = 0.88, rely = 0.15,
                            relwidth = 0.08, relheight = 0.25, command = self.register)
        
        self.update_button = Button(master = self, text = "🔄", relx = 0.88, rely = 0.6,
                            relwidth = 0.08, relheight = 0.25, command = self.update)
        
    def register(self) -> None:
        conn  = sqlite3.connect("events.db")
        cursor = conn.cursor()
        
        accredited = "yes" if self.accredited == "no" else "no"
        instruction = f"UPDATE {self.database} SET Acreditado='{accredited}' WHERE Nombre='{self.name}' AND Bufete='{self.office}'"
        cursor.execute(instruction)

        conn.commit()
        conn.close()
        
        self.master.master.master.master.current_database_of_accredited(self.database)
        
    def update(self) -> None:  
        try:   
            self.destroy_name_entry()
            self.destroy_category_entry()
        except:
            self.change_name = Entry(master = self, relx = 0.05, rely = 0.2, relwidth = 0.8, relheight = 0.3, 
                                placeholder_text = self.name)
            self.change_name.bind("<Return>", lambda event: self.change_name_and_destroy())
        
            self.change_category = Entry(master = self, relx = 0.05, rely = 0.6, relwidth = 0.8, relheight = 0.2, 
                                placeholder_text = self.office)
            self.change_category.bind("<Return>", lambda event: self.change_category_and_destroy())
            
            self.check.configure(text = "X", command = self.delete)
        
    def change_name_and_destroy(self) -> None:
        if not self.change_name.get():
            self.destroy_name_entry()
            return 
        
        self.name_label.configure(text = self.change_name.get().title())
        
        instruction = f"UPDATE {self.database} SET Nombre='{self.change_name.get().title()}' WHERE Nombre='{self.name}' AND Bufete='{self.office}'"
        self.query(instruction)
        self.name = self.change_name.get().title()
        self.destroy_name_entry()
        
    def destroy_name_entry(self) -> None:
        self.change_name.destroy()
        try:
            self.change_category.focus_set()
        except:
            self.master.master.master.master.current_database_of_accredited(self.database)
        
    def change_category_and_destroy(self) -> None:
        if not self.change_category.get():
            self.destroy_category_entry()
            return 
        
        self.office_label.configure(text = f"Bufete/Cat: {self.change_category.get().title()}")
        
        instruction = f"UPDATE {self.database} SET Bufete='{self.change_category.get().title()}' WHERE Nombre='{self.name}' AND Bufete='{self.office}'"
        self.query(instruction)
        self.office = self.change_category.get().title()
        self.destroy_category_entry()
        
        
    def destroy_category_entry(self) -> None:
        self.change_category.destroy()
        try:
            self.change_name.focus_set()
        except:
            self.master.master.master.master.current_database_of_accredited(self.database)
        
    def query(self, instruction: str) -> None:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()

        cursor.execute(instruction)

        conn.commit()
        conn.close()
        
    def delete(self) -> None:
        self.query(f"DELETE FROM {self.database} WHERE Nombre='{self.name}' AND Bufete='{self.office}'")
        self.master.master.master.master.current_database_of_accredited(self.database)


####################
# EVENT NAME FRAMES
####################
@dataclass
class InterfaceEventNameFrames(ABC, ctk.CTkFrame):
    """Interface to generate event name frames for Recorver Frame"""
    master: ctk.CTkFrame
    table_name: str
    
    @abstractmethod
    def __post_init__(self) -> None:
        ctk.CTkFrame.__init__(self, master = self.master, fg_color = "white", height = 70)
        self.widgets()
        
        self.pack(expand = True, fill = "x", padx = 5, pady = 5)
        
    def widgets(self) -> None:
        self.name_font = font = ctk.CTkFont("Arial", 15, "bold")
        self.date_font = font = ctk.CTkFont("Arial", 15)
        
        name = " ".join(self.table_name[:-8].split("_"))
        date = self.table_name[-8:][:2] + "-" + self.table_name[-8:][2:4] + "-" + self.table_name[-8:][4:] 
        
        self.name_label = Label(master = self, text = name, text_color = "black", font = self.name_font, 
                             relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.35)
        self.name_label.bind("<Button>", lambda event: self.event())
        
        self.date_label = Label(master = self, text = f"Fecha: {date}", text_color = "#77767b", font = self.date_font, 
                             relx = 0.05, rely = 0.6, relwidth = 0.6, relheight = 0.2)
        self.date_label.bind("<Button>", lambda event: self.event())
    
        self.bind("<Button>", lambda event: self.event())
    
    def event(self) -> None:
        self.master.master.master.master.master.current_database_of_accredited(self.table_name)
        self.master.master.master.master.master.new_panel_frame.cancel()
        self.master.master.master.master.master.recorver_event.cancel()
        self.master.master.master.master.master.event_name.configure(text = f"Evento: {' '.join(self.table_name[:-8].split('_'))}")
        
        
@dataclass
class EventNameFrames(InterfaceEventNameFrames):
    """Class to create concrete event name frames for Recorver Frame"""
    def __post_init__(self) -> None:
        InterfaceEventNameFrames.__post_init__(self)