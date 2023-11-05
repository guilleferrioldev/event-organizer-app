import customtkinter as ctk
from dataclasses import dataclass 
from abc import ABC, abstractmethod
from interfaces import InterfaceSlidingFrame

@dataclass
class NewEvent(InterfaceSlidingFrame):
    """Class to create concrete button"""
    def __post_init__(self):
        InterfaceSlidingFrame.__post_init__(self)   