import customtkinter as ctk
from settings import *
from func_clases import *
from datetime import datetime
from tkinter import messagebox

class GestorLogistica(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)