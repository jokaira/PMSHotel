# librerias de interfaz grafica
import customtkinter as ctk
from tkinter import ttk

#librerias y modulos de funcionamiento del sistema
import sqlite3 as sql
from gestor_clientes import GestorClientes #modulo de clientes
from Main_Habitaciones import * #modulo de habitaciones
from Calendario_de_Reserva import * #modulo de reservas

# configuracion del modo de apariencia y tema de colores
ctk.set_appearance_mode("light") #modo claro
ctk.set_default_color_theme("blue") #tema azul

res_ventana = {"x": 1200, "y": 800} #variable de la resolución de la ventana principal


class Main(ctk.CTk):
    #clase principal que representa la ventana principal
    def __init__(self):
        super().__init__() #constructor

        #config basica de la ventana
        self.title("PMS Hotel - Sistema de Gestión Hotelera") #titulo
        self.geometry(f"{res_ventana['x']}x{res_ventana['y']}") #tamaño de ventana
        self.resizable(True, True) #redimensionamiento
        self.configure(bg="#f8f9fa") #fondo gris claro

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("My.TFrame", background = "white")

        # frame para los botones de los distintos módulos
        self.principal = ttk.Frame(self, 
                                   width=res_ventana["x"]*0.90, 
                                   height=res_ventana["y"]*0.90,
                                   style = "My.TFrame")
        self.principal.place(relx=0.5, rely=0.5, anchor="center")

        #botón para acceder al gestor de clientes
        self.clientes = GestorClientes(self)
        self.boton_clientes = ttk.Button(self.principal, text="Gestor de Clientes", command=self.abrir_gestor_clientes)
        self.boton_clientes.place(relx=0.5, rely=0.5, anchor="center")

        #boton para acceder al gestor de habitaciones
        self.habitaciones = GestionDeHabitacionesApp(self)
        self.boton_habitaciones = ttk.Button(self.principal, text="Gestor de Habitaciones", command=self.abrir_gestor_habitaciones)
        self.boton_habitaciones.place(relx=0.5, rely=0.25, anchor="center")

        #boton para acceder al gestor de reservas
        self.reservas = CalendarioReservasApp(self)
        self.boton_reservas = ttk.Button(self.principal, text="Gestor de Reservas", command=self.abrir_gestor_reservas)
        self.boton_reservas.place(relx=0.5, rely=0.75, anchor="center")
    
    def abrir_gestor_clientes(self):
        self.principal.place_forget()
        self.clientes.place(relx=0.5, rely=0.5, anchor="center")

    def atras_clientes(self): #esto es para cuando se le da a atras desde el gestor de clientes
        self.clientes.place_forget()
        self.principal.place(relx=0.5, rely=0.5, anchor="center")

    def abrir_gestor_habitaciones(self):
        self.principal.place_forget()
        self.habitaciones.place(relx=0.5, rely=0.5, anchor="center")
    
    def atras_habitaciones(self): #esto es pa cuando se le da a atras desde el gestor de habitaciones
        self.habitaciones.place_forget()
        self.principal.place(relx=0.5, rely=0.5, anchor="center")
    
    def abrir_gestor_reservas(self):
        self.principal.place_forget()
        self.reservas.place(relx=0.5, rely=0.5, relwidth=1.0, relheight=1.0, anchor="center")
        self.reservas.setup_ui()
    
    def atras_reservas(self): #esto es pa cuando se le da a atras desde el gestor de reservas
        self.reservas.place_forget()
        self.principal.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = Main()
    app.mainloop()