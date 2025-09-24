#librerias
import customtkinter as ctk #UI

#ajustes y funciones
from settings import *
import basedatos
from func_clases import *

#módulos
from dashboard import *
from clientes import * 
from habitaciones import *
from reservas import *
from logistica import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=CLARO)

        ctk.set_appearance_mode('light')
        self.title("PMS Hotel")
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')
        
        #inicia la verificacion de las tablas de la base de datos
        basedatos.conectar_bd()
        basedatos.verificar_tablas()

        #encabezado
        Header(self)

        #contenedor de los módulos
        self.main_frame = MainFrame(self, texto='')

        #modulos
        self.dashboard = None
        self.clientes = None
        self.habitaciones = None
        self.reservas = None
        self.logistica = None

        #menu lateral con botones
        self.sidebar = SideBar(self)

        self.btn_dashboard = self.sidebar.crear_boton_nav(BTN_HEAD[0], metodo=self.mostrar_dashboard)
        self.btn_dashboard.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_clientes = self.sidebar.crear_boton_nav(BTN_HEAD[1], metodo=self.mostrar_clientes)
        self.btn_clientes.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_habitaciones = self.sidebar.crear_boton_nav(BTN_HEAD[2], metodo=self.mostrar_habitaciones)
        self.btn_habitaciones.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_reservas = self.sidebar.crear_boton_nav(BTN_HEAD[3], metodo=self.mostrar_reservas)
        self.btn_reservas.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_logistica = self.sidebar.crear_boton_nav(BTN_HEAD[4], metodo=self.mostrar_logistica)
        self.btn_logistica.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        #cada vez que se agregue un módulo, hay que agregar su correspondiente botón y método

        #dashboard por default
        self.mostrar_dashboard()

    def limpiar_mainframe(self):
        # limpia el frame que contiene los módulos
        for widget in self.main_frame.modulos.winfo_children():
            widget.destroy()

    def inactivar_botones(self):
        self.btn_dashboard.configure(fg_color = 'transparent')
        self.btn_clientes.configure(fg_color = 'transparent')
        self.btn_habitaciones.configure(fg_color = 'transparent')
        self.btn_reservas.configure(fg_color = 'transparent')
        self.btn_logistica.configure(fg_color = 'transparent')
    
    def mostrar_dashboard(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[0])
        self.btn_dashboard.configure(fg_color = '#34495e')
        self.dashboard = Dashboard(self.main_frame.modulos)

    def mostrar_clientes(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[1])
        self.btn_clientes.configure(fg_color = '#34495e')
        self.clientes = GestorClientes(self.main_frame.modulos)

    def mostrar_habitaciones(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[2])
        self.btn_habitaciones.configure(fg_color = '#34495e')
        self.habitaciones = GestorHabitaciones(self.main_frame.modulos)

    def mostrar_reservas(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[3])
        self.btn_reservas.configure(fg_color = '#34495e')
        self.reservas = GestorReservas(self.main_frame.modulos)

    def mostrar_logistica(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[4])
        self.btn_logistica.configure(fg_color = '#34495e')
        self.logistica = GestorLogistica(self.main_frame.modulos)

class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color=PRIMARIO, corner_radius=0,
                         height = 43)

        self.place(x = 0, y = 0, relwidth = 1)
        self.pack_propagate(False)

        #texto encabezado
        ctk.CTkLabel(self, 
                     text='🏨 PMS Hotel · Sistema de Gestión Hotelera', 
                     text_color=BLANCO,
                     font = (FUENTE,TAMANO_TEXTO_DEFAULT,'bold'),
                     ).pack(side='left', padx = 12)

class SideBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, corner_radius=0, fg_color=OSCURO, 
             width = 240)
        
        self.place(x= 0, y = 42, relheight=1)
        self.pack_propagate(False)

        #titulo del menu lateral
        ctk.CTkLabel(self, 
                     text='Módulos', 
                     text_color=BLANCO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(padx = (6+16,0+16), pady = (0+16,12+16), anchor = 'w')
    
        self.nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.nav_frame.pack(fill='both', expand=True)

    def crear_boton_nav(self, texto, metodo):
        return ctk.CTkButton(
            master = self.nav_frame,
            text=texto,
            text_color= BLANCO,
            fg_color= '#34495e',
            hover_color='#34495e',
            corner_radius=8,
            font=(FUENTE, TAMANO_TEXTO_DEFAULT),
            anchor = 'w',
            command=metodo
        )

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, texto):
        super().__init__(master=master, fg_color='transparent')
        self.place(x = 0, y = 42, relheight = 1, relwidth = 1)

        self.rowconfigure(index=1, weight=1, uniform='b')
        self.columnconfigure(index=0, weight=1, uniform='b')

        self.titulo = ctk.CTkFrame(self, fg_color=PRIMARIO,corner_radius= 10, height = 39)
        self.titulo.grid(row = 0, column = 0, sticky = 'nsew', padx = (16 + 240, 16), pady = (16,8))

        self.label_titulo =ctk.CTkLabel(self.titulo, 
                     text=texto,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'),
                     text_color=BLANCO
                     )
        self.label_titulo.pack(side = 'left', padx = 16, pady = 6)

        #contenedor de los módulos
        self.modulos = ctk.CTkFrame(self, fg_color='transparent')
        self.modulos.grid(row = 1, column = 0, sticky = 'nsew', padx = (16 + 240, 16), pady = (8,16+43))
        self.modulos.pack_propagate(False)

if __name__ == '__main__':
    window = App()
    window.mainloop()