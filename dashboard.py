import customtkinter as ctk
from settings import *
from func_clases import *
import clientes
import basedatos

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        self.rowconfigure(index=0, weight=0, minsize=109)
        self.rowconfigure(index=1, weight=0, minsize=100)
        self.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')


        #crear tarjetas kpi
        crear_tarjetas_kpi(master=self, dict=KPI_DASHBOARD())
        
        #botones de acciones rápidas
        self.acciones_rapidas()

    def acciones_rapidas(self):
        contenedor = ctk.CTkFrame(self, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=100)
        contenedor.grid(row = 1, column =0, columnspan= 4, sticky = 'nsew')
        contenedor.grid_propagate(False)

        contenedor.rowconfigure(index=0, weight = 1)
        contenedor.rowconfigure(index=1, weight = 1)
        contenedor.columnconfigure(index=0, weight = 1, uniform='d')

        ctk.CTkLabel(contenedor, 
                     text='Acciones Rápidas', 
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).grid(row=0, column = 0, sticky = 'w', padx = 12, pady = (12,0))
        
        #contenedor de botones
        btn_cont = ctk.CTkFrame(contenedor, fg_color='transparent', height=37)
        btn_cont.grid(row = 1, column = 0, sticky = 'nsew', padx = 12, pady = (6,12))
        btn_cont.grid_propagate(False)

        #nuevo cliente
        Boton(master=btn_cont,
              texto = '➕ Nuevo Cliente',
              metodo= self.winfo_toplevel().mostrar_clientes
              )

        #nueva habitación
        Boton(master=btn_cont,
              texto='🏠 Nueva Habitación',
              color= PRIMARIO,
              hover= ROJO,
              metodo=self.winfo_toplevel().mostrar_habitaciones
              )

        #nueva reserva
        Boton(master=btn_cont,
              texto='📅 Nueva Reserva',
              color=VERDE1,
              hover=VERDE2,
              metodo=self.winfo_toplevel().mostrar_reservas
              )
        
        #insertar datos de muestra
        Boton(master=btn_cont,
              texto = '📝 Insertar datos de muestra',
              color=MAMEY,
              hover=MAMEY2,
              metodo=self.datos_muestra
              )
        
        #limpiar base de datos
        Boton(master=btn_cont,
              texto = '🗑️ Borrar todos los datos',
              color=OSCURO,
              hover=MUTE,
              metodo=self.limpiar_datos
              )
    
    def datos_muestra(self):
        basedatos.insertar_datos_muestra()
        from settings import KPI_DASHBOARD
        crear_tarjetas_kpi(master=self, dict=KPI_DASHBOARD())
    
    def limpiar_datos(self):
        basedatos.limpiar_datos()
        from settings import KPI_DASHBOARD
        crear_tarjetas_kpi(master=self, dict=KPI_DASHBOARD())
