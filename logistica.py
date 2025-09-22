import customtkinter as ctk
from settings import *
from func_clases import *
from datetime import datetime
from tkinter import messagebox

class GestorLogistica(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #pestañas
        self.contenedor_pestanas = ctk.CTkFrame(master=self, fg_color='transparent')
        self.contenedor_pestanas.pack(anchor = 'n',fill = 'x', pady = (0,10))
        self.boton_pestanas(master=self.contenedor_pestanas)

        self.logistica = ctk.CTkFrame(master=self, fg_color='transparent', border_color=GRIS_CLARO3, corner_radius=10, border_width=0)
        self.logistica.pack(anchor = 'n', fill = 'x')

        self.housekeeping()

    def boton_pestanas(self, master):
            self.btn_housekeeping = ctk.CTkButton(master=master, 
                          text= 'Housekeeping',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.housekeeping,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_housekeeping.pack(side ='left')

            self.btn_mantenimiento = ctk.CTkButton(master=master, 
                          text= 'Mantenimiento',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_mantenimiento.pack(side ='left', padx = (10,5))

            self.btn_inventario = ctk.CTkButton(master=master, 
                          text= 'Inventario',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_inventario.pack(side ='left', padx = 5)

            self.btn_personal = ctk.CTkButton(master=master, 
                          text= 'Personal',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_personal.pack(side ='left', padx = 5)

    def housekeeping(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_housekeeping.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 1)

        #kpi de housekeeping
        self.kpis = ctk.CTkFrame(master=self.logistica, fg_color='transparent', corner_radius=0)
        self.kpis.pack(anchor = 'n',fill = 'x')

        self.kpis.rowconfigure(index=0, weight=0, minsize=109)
        self.kpis.rowconfigure(index=1, weight=0)
        self.kpis.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')
        crear_tarjetas_kpi(master=self.kpis, dict=KPI_HOUSEKEEPING())

        