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

        # definición de estilos de los widgets
        self.style = ttk.Style() #objeto estilo
        self.style.theme_use("clam") #tema
        
        #colores de botones 
        self.style.configure("TButton", #"themed button"
                             foreground = "white", #texto blanco
                             background = "#c0392b", #fondo rojo
                             font = ("Arial", 12, "bold"), #arial tamaño 12 en negrita
                             padding = (20,10)) #padding horizontal de 20, y vertical de 10

        #configuración de los estados del boton (hover y presionado)
        self.style.map("TButton", #establece estilo dinámico (para cada estado del botón)
                       background = [("active", "#e74c3c"), ("pressed", "#a93226")], #colores para hover (active) y para presionado (pressed)
                       foreground = [("active", "#fff")]) #color del texto en hover
        
        #encabezados de las tablas
        self.style.configure("Treeview.Heading", #este selecciona los encabezados
                             background = "#c0392b", #fondo rojo
                             foreground = "white", #letra blanca
                             font = ("Arial", 11, "bold")) #arial tamaño 11 negrita

        #filas de las tablas
        self.style.configure("Treeview", #este selecciona las filas
                             background = "#fff", #fondo de las filas
                             fieldbackground = "#fff", #fondo de la tabla completa (incluyendo las filas vacías)
                             font = ("Arial", 10), #arial tamaño 10
                             rowheight = 30) #altura de 30px para las filas

        #contenedor principal
        self.main_container = ctk.CTkFrame(self, fg_color= "transparent") #frame con fondo transparente
        self.main_container.pack(fill = "both", #para que se expanda en ambas direcciones (vertical y horizontal)
                                 expand = True, #para que se expanda en todo el espacio
                                 padx = 20, pady = 20) #padding

        #encabezado del programa
        self.create_header() #metodo para crear el encabezado

        #contenedor de la barra de navegacion lateral
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color = "transparent")
        self.content_frame.pack(fill = "both", expand = True, pady = (20, 0)) #padding de 20 arriba y 0 abajo

        #barra de navegacion lateral
        self.create_sidebar() #metodo para crear la barra lateral

        #frame para el contenido principal
        self.main_content = ctk.CTkFrame(self.content_frame, fg_color = "#fff", corner_radius = 15)
        self.main_content.pack(side = "left", fill = "both", expand = True, padx = (20, 0))

        #inicialización de módulos
        self.clientes = None #modulo de clientes
        self.habitaciones = None #modulo de habitaciones
        self.reservas = None #modulo de reservas
        #TODO: agregar mas modulos

        #esto muestra el dashboard por defecto
        self.show_dashboard() #metodo para mostrar el dashboard
    
    def create_header(self):
        #crea encabezado con titulo y el branding, logo e info de la "empresa"
        
        #frame del encabezado con color rojo y esquinas redondeadas
        header_frame = ctk.CTkFrame(self.main_container, 
                                    fg_color = "#c0392b",
                                    corner_radius = 15, #esquina con radio de 15px
                                    height = 80) #altura de 80px
        header_frame.pack(fill = "x", #se expandirá solo horizontalmente
                          pady = (0, 20)) #padding superior de 0 e inferior de 20
        header_frame.pack_propagate(False) #evita redimensionamiento por los widgets

        #titulo
        title_label = ctk.CTkLabel(header_frame, 
                                   text = "🏨 PMS Hotel", #ante falta de logo, se coloca un emoji
                                   font = ("Arial", 28, "bold"), #arial tamaño 28 negrita
                                   text_color = "white") #letra color blanco
        title_label.pack(side = "left", #alineado a la izquierda
                         padx = 30, pady = 20)

        # subtitulo
        subtitle_label = ctk.CTkLabel(header_frame, text = "Sistema de Gestión Hotelera", font = ("Arial", 14), text_color = "#f8f9fa")
        subtitle_label.pack(side = "left", padx = (10, 0), #padding de 10px a la izquierda y 0 a la derecha
                            pady = 20)

    def create_sidebar(self):
        #crea la barra de navegacion lateral con los botones de los módulos

        #frame de la barra lateral
        sidebar_frame = ctk.CTkFrame(self.content_frame, fg_color = "#2c3e50", #fondo de color azul oscuro
                                     corner_radius = 15, width = 250)
        sidebar_frame.pack(side = "left", fill = "y", #se expande solo a lo vertical
                           padx = (0, 20)) #padding de 0 a la izquiera y 20px a la derecha
        sidebar_frame.pack_propagate(False)

        #titulo de barra lateral
        sidebar_title = ctk.CTkLabel(sidebar_frame, text = "Módulos", font = ("Arial", 18, "bold"), text_color= "white")
        sidebar_title.pack(pady = (30, 20))

        #definicion de estilo para los botones de navegacion
        button_style = {
            "fg_color": "transparent", #color del boton
            "text_color": "white", #color del texto
            "font": ("Arial", 14, "bold"),
            "corner_radius": 10,
            "height": 50, #altura del boton
            "hover_color": "#34495e"
        }

        #boton de Dashboard
        self.btn_dashboard = ctk.CTkButton(sidebar_frame, text = "📊 Dashboard", command = self.show_dashboard, **button_style)#aplica el estilo definido anteriormente
        self.btn_dashboard.pack(fill = "x", padx = 20, pady = 5)

        #boton de Gestor de Clientes
        self.btn_clientes = ctk.CTkButton(sidebar_frame, text = "👥 Gestor de Clientes", command = self.abrir_gestor_clientes, **button_style)
        self.btn_clientes.pack(fill = "x", padx = 20, pady = 5)

        #boton de Gestor de Habitaciones
        self.btn_habitaciones = ctk.CTkButton(sidebar_frame, text = "🏠 Gestor de Habitaciones", command = self.abrir_gestor_habitaciones, **button_style)
        self.btn_habitaciones.pack(fill = "x", padx = 20, pady = 5)
    
        #boton de Gestor de Reservas
        self.btn_reservas = ctk.CTkButton(sidebar_frame, text = "📅 Gestor de Reservas", command = self.abrir_gestor_reservas, **button_style)
        self.btn_reservas.pack(fill = "x", padx = 20, pady = 5)

        #espacio adicional al final de la barra
        spacer = ctk.CTkFrame(sidebar_frame, fg_color = "transparent", height = 50)
        spacer.pack(fill = "x", pady = 20)
    
    def clear_main_content(self):
        #limpia el frame de contenido principal
        #elimina todos los widgets
        for widget in self.main_content.winfo_children(): #este metodo devuelve una lista con todos los widgets que estén dentro de ese contenedor
            widget.destroy()

    def show_dashboard(self):
        #muestra el dashboard con estadisticas, tarjetas y botones de accion rápida

        self.clear_main_content() #limpia el frame del contenido principal

        #frame del dashboard
        dashboard_frame = ctk.CTkFrame(self.main_content, fg_color = "transparent")
        dashboard_frame.pack(fill = "both", expand = True, padx = 30, pady = 30)

        #mensaje de bienvenida
        welcome_label = ctk.CTkLabel(dashboard_frame,
                                     text = "¡Bienvenido al Sistema de Gestión Hotelera!",
                                     font = ("Arial", 24, "bold"),
                                     text_color = "#2c3e50")
        welcome_label.pack(pady = (0, 20))

        #frame para las tarjetas de estadisticas
        stats_frame = ctk.CTkFrame(dashboard_frame)
        stats_frame.pack(fill = "x", pady = 20)

        #tarjetas de las estadisticas
        self.create_stat_card(stats_frame, "👥 Clientes", 
                              "150",#TODO: por el momento no tendrá un cálculo
                              "#3498db", 0)
        self.create_stat_card(stats_frame, "🏠 Habitaciones", 
                              "45",
                              "#e74c3c", 1)
        self.create_stat_card(stats_frame, "📅 Reservas Activas", 
                              "23",
                              "#2ecc71", 2)
        self.create_stat_card(stats_frame, "💰 Ingresos del Mes", 
                              "$15,420",
                              "#f39c12", 3)
        
        #frame para acciones rápidas
        actions_frame = ctk.CTkFrame(dashboard_frame, fg_color = "transparent")
        actions_frame.pack(fill = "x", pady = 30)

        # creacion de titulo de acciones rapidas
        actions_label = ctk.CTkLabel(
            actions_frame,
            text = "Acciones Rápidas",
            font = ("Arial", 18, "bold"),
            text_color = "#2c3e50"
        )
        actions_label.pack(pady = (0, 20))

        #frame para botones de accion rápida
        quick_actions = ctk.CTkFrame(actions_frame, fg_color = "transparent")
        quick_actions.pack(fill = "x")

        #definicion de estilo de los botones
        quick_btn_style = {
            "fg_color": "#c0392b",
            "text_color": "white",
            "font": ("Arial", 12, "bold"),
            "corner_radius": 10,
            "height": 40,
            "hover_color": "#e74c3c"
        }

        #boton para agregar nuevo cliente
        ctk.CTkButton(
            quick_actions,
            text = "➕ Nuevo Cliente",
            command = self.abrir_gestor_clientes, #TODO: hay que crear o modificar funciones que directamente te lleve al gestor y abra el toplevel
            **quick_btn_style
        ).pack(side = "left", padx = (0, 10))

        #boton para agregar nueva habitacion
        ctk.CTkButton(
            quick_actions,
            text = "🏠 Nueva Habitación",
            command = self.abrir_gestor_habitaciones, 
            **quick_btn_style
        ).pack(side = "left", padx = (0, 10))

        #boton para agregar nueva reserva
        ctk.CTkButton(
            quick_actions,
            text = "📅 Nueva Reserva",
            command = self.abrir_gestor_reservas, #aqui el TODO no aplica
            **quick_btn_style
        ).pack(side = "left")

    def create_stat_card(self, master, titulo, valor, color, columna):
        #crea tarjeta de estadísticas
        #argumentos:
            # master: el que contendrá la tarjeta
            # titulo: el titulo de la estadistica
            # valor: el numero a mostrar
            # color: el color de la tarjeta
            # columna: el numero de la columna, por el momento no se usa
        
        #frame de cada tarjeta
        card = ctk.CTkFrame(master, fg_color = color, corner_radius = 15, height = 120)
        card.pack(side = "left", fill = "both", expand = True, padx = (0, 10))

        #titulo de la tarjeta
        title_label = ctk.CTkLabel(
            card,
            text = titulo,
            font = ("Arial", 14, "bold"),
            text_color = "white"
        )
        title_label.pack(pady = (20, 5))

        #valor de la estadistica
        value_label = ctk.CTkLabel(
            card,
            text = valor,
            font = ("Arial", 24, "bold"),
            text_color = "white"
        )
        value_label.pack()

    def abrir_gestor_clientes(self):
        #abre y muestra el modulo de gestión de clientes
        self.clear_main_content()
        self.clientes = GestorClientes(self.main_content)
        self.clientes.pack(fill = "both", expand = True, padx = 20, pady = 20)

    def atras_clientes(self): #esto es para cuando se le da a atras desde el gestor de clientes
        if self.clientes:
            self.clientes.pack_forget()
        self.show_dashboard()

    def abrir_gestor_habitaciones(self):
        #abre y muestra el modulo de habitaciones
        self.clear_main_content()
        self.habitaciones = GestionDeHabitacionesApp(self.main_content)
        self.habitaciones.pack(fill = "both", expand = True, padx = 20, pady = 20)
    
    def atras_habitaciones(self): #esto es pa cuando se le da a atras desde el gestor de habitaciones
        if self.habitaciones:
            self.habitaciones.pack_forget()
        self.show_dashboard()
    
    def abrir_gestor_reservas(self):
        #abre el modulo de reservas
        self.clear_main_content()
        self.reservas = CalendarioReservasApp(self.main_content)
        self.reservas.pack(fill = "both", expand = True, padx = 20, pady = 20)
        self.reservas.setup_ui()
    
    def atras_reservas(self): #esto es pa cuando se le da a atras desde el gestor de reservas
        if self.reservas:
            self.reservas.pack_forget()
        self.show_dashboard()


if __name__ == "__main__":
    app = Main()
    app.mainloop()