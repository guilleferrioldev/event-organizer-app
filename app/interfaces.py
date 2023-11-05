import customtkinter as ctk 
from dataclasses import dataclass 
from abc import ABC, abstractmethod
from typing import List, Callable
from PIL import Image


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
    def __post_init__(self):
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
    def __post_init__(self):
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
    def __post_init__(self):
        ctk.CTkScrollableFrame.__init__(self, master = self.master)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
@dataclass
class Scrollable(InterfaceScrollableFrame):
    """Class to create concrete scrollable frames"""
    def __post_init__(self):
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
    
    @abstractmethod
    def __post_init__(self):
        ctk.CTkEntry.__init__(self, master = self.master, placeholder_text = "Buscar", font = ctk.CTkFont("Arial", 15))
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)


@dataclass
class Entry(InterfaceEntry):
    """Class to create concrete entry"""
    def __post_init__(self):
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
    
    @abstractmethod
    def __post_init__(self):
        ctk.CTkOptionMenu.__init__(self, master = self.master, values = self.values, fg_color = "#860505", button_color = "red", 
                                   button_hover_color = "#860505", dropdown_hover_color = "red", font = ctk.CTkFont("Arial", 15))
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)


@dataclass
class Menu(InterfaceMenu):
    """Class to create concrete option menu"""
    def __post_init__(self):
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
    
    @abstractmethod
    def __post_init__(self):
        ctk.CTkButton.__init__(self, master = self.master, text = self.text, font = ctk.CTkFont("Arial", 12),
                               fg_color= "#860505", hover_color = "red", command = self.command)
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
        
@dataclass
class Button(InterfaceButton):
    """Class to create concrete button"""
    def __post_init__(self):
        InterfaceButton.__post_init__(self)   
        
  
####################
# IMAGE BUTTON
#################### 
@dataclass
class InterfaceImageButton(ABC, ctk.CTkButton):
    """Interface to generate image buttons"""
    master: ctk.CTkFrame
    path: str
    #command: Callable
    relx: float
    rely: float
    relwidth: float
    relheight: float
    
    @abstractmethod
    def __post_init__(self):
        the_image = ctk.CTkImage(light_image = Image.open(self.path), size = (120, 130))
        ctk.CTkButton.__init__(self, master = self.master,text = "", image = the_image, fg_color = "#860505", hover_color = "red")
        
        self.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)
 
@dataclass
class ImageButton(InterfaceImageButton):
    """Class to create concrete image button"""
    def __post_init__(self):
        InterfaceImageButton.__post_init__(self)   
        
           
####################
# SLIDING FRAME
####################       
@dataclass
class InterfaceSlidingFrame(ABC, ctk.CTkFrame):
    """Interface to generate slide frames"""
    master: ctk.CTkFrame
    start_pos: float
    end_pos: float
    
    @abstractmethod
    def __post_init__(self):
        ctk.CTkFrame.__init__(self, master = self.master, fg_color = "#77767b")
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        self.font = ctk.CTkFont("Arial", 15, "bold")
        self.widgets()
        
        self.place(relx = self.start_pos, rely = 0.25)
        
    @abstractmethod
    def widgets(self):
        pass
        
    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = 0.25, rely = 0.25, relwidth = 0.45, relheight = 0.5)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.25)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True
            
####################
# FRAMES
####################
@dataclass
class InterfaceFrame(ABC, ctk.CTkFrame):
    """Interface to generate frames"""
    master: ctk.CTkFrame
    name: str
    office: str
    position: str
    
    @abstractmethod
    def __post_init__(self):
        ctk.CTkFrame.__init__(self, master = self.master, fg_color = "white", height = 100)
        self.widgets()
        
        self.pack(expand = True, fill = "x", padx = 5, pady = 5)
    
    def widgets(self):
        self.name_font = font = ctk.CTkFont("Arial", 15, "bold")
        self.other_font = font = ctk.CTkFont("Arial", 15)
        
        self.name_label = Label(master = self, text = self.name, text_color = "#860505", font = self.name_font, 
                             relx = 0.05, rely = 0.2, relwidth = 0.8, relheight = 0.2)
        
        self.office_label = Label(master = self, text = f"Bufete: {self.office}", text_color = "#77767b", font = self.other_font, 
                             relx = 0.05, rely = 0.45, relwidth = 0.6, relheight = 0.2)
        
        self.position_label = Label(master = self, text = f"Cargo: {self.position}", text_color = "#77767b", font = self.other_font, 
                             relx = 0.05, rely = 0.65, relwidth = 0.6, relheight = 0.2)

@dataclass
class FrameToRegister(InterfaceFrame):
    """Class to create concrete image button"""
    def __post_init__(self):
        InterfaceFrame.__post_init__(self)  
        self.check = Button(master = self, text = "+", relx = 0.88, rely = 0.12,
                            relwidth = 0.08, relheight = 0.25, command = self.register)
        
    def register(self):
        print("registrar")

