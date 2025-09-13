import customtkinter as ctk
from settings import *
from func_clases import *

class GestorReservas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        self.rowconfigure(index=0, weight=0, minsize=109)
        self.rowconfigure(index=1, weight=0)
        self.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')

        #kpi de reservas
        crear_tarjetas_kpi(master=self, dict=KPI_RESERVAS())

        #pestañas con sus ventanitas
        self.opciones_reservas()

    def opciones_reservas(self):
        tabview = ctk.CTkTabview(master=self, 
                                 fg_color='transparent',
                                 border_color=GRIS_CLARO3, 
                                 border_width=1, 
                                 segmented_button_fg_color=CLARO,
                                 segmented_button_selected_color=AZUL_CLARO,
                                 segmented_button_unselected_color=GRIS_CLARO4,
                                 segmented_button_selected_hover_color=AZUL2,
                                 segmented_button_unselected_hover_color=GRIS_CLARO3,
                                 text_color=OSCURO
                                 )
        tabview.grid(row = 1, column = 0, columnspan = 4, sticky = 'nsew')

        #pestañas
        self.tab1 = tabview.add('➕ Nueva Reserva')
        self.tab2 = tabview.add('🔍 Buscar Disponibilidad')
        self.tab3 = tabview.add('📋 Gestionar Reservas')
        self.tab4 = tabview.add('📚 Historial')
        # self.tab5 = tabview.add('📅 Vista Calendario') #TODO:posible mejora, agregar el asunto de la visualización por calendario
        tabview.set('➕ Nueva Reserva')

        self.nueva_reserva()
        self.buscar_disponibilidad()
        self.gestionar_reservas()
        self.historial_reservas()
    
    def nueva_reserva(self):
        ctk.CTkLabel(master=self.tab1, 
                     text= '📝 Crear Nueva Reserva',
                     text_color=PRIMARIO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(pady = 6, padx = 12, anchor = 'w')
  
        ctk.CTkLabel(master=self.tab1, 
                     text= '👤 Cliente',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).pack(anchor = 'w', pady = 6, padx = 12)
        
        frame_buscador = ctk.CTkFrame(self.tab1, fg_color='transparent')
        frame_buscador.pack(fill = 'x', expand = True)
        
        ctk.CTkEntry(master=frame_buscador,
                     placeholder_text='Buscar cliente por nombre, email o teléfono...',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35, width = 335
                     ).pack(side = 'left',pady = 6, padx = (12,5))
        
        ctk.CTkButton(master = frame_buscador, 
                            text = '🔍 Buscar', 
                            fg_color=AZUL, 
                            hover_color=AZUL2,
                            text_color=BLANCO,font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                            corner_radius=10,
                            ).pack(side = 'left', padx = (0,5))
        
        ctk.CTkButton(master = frame_buscador, 
                            text = '➕ Nuevo', 
                            fg_color=VERDE1, 
                            hover_color=VERDE2,
                            text_color=BLANCO,font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                            corner_radius=10,
                            ).pack(side = 'left', padx = (0,5))

        frame_datos_reserva = ctk.CTkFrame(self.tab1, fg_color='transparent')
        frame_datos_reserva.pack(fill = 'x', expand = True)
        frame_datos_reserva.columnconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='z')
        frame_datos_reserva.rowconfigure(index=(0,1,2), weight=1, uniform='z')

        #Frame con los datos del cliente. TODO: Agregar y colocar funcion

        #Fecha de Entrada
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '📅 Fecha de Entrada',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx = 5)

        fecha_entrada_entry = CTkDatePicker(master=frame_datos_reserva)
        fecha_entrada_entry.grid(row = 0, column = 3, sticky = 'nsew')
        fecha_entrada_entry.set_date_format('%d-%m-%Y')
        fecha_entrada_entry.set_localization('es_ES')
        fecha_entrada_entry.set_allow_manual_input(True)

        #Fecha de Salida
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '📅 Fecha de Salida',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 4, sticky = 'w', padx = 5)
        
        fecha_salida_entry = CTkDatePicker(master=frame_datos_reserva)
        fecha_salida_entry.grid(row = 0, column = 5, sticky = 'nsew')
        fecha_salida_entry.set_date_format('%d-%m-%Y')
        fecha_salida_entry.set_localization('es_ES')
        fecha_salida_entry.set_allow_manual_input(True)

        #Tipo de habitación
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '🏠 Tipo de Habitación',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 6, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=frame_datos_reserva,
                        values = ['Cualquier tipo', 'Individual', 'Doble', 'Suite'],#TODO: atarlo a la base de datos
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).grid(row = 0, column = 7, sticky = 'nsew')
        
        #Tipo de reserva
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '👥 Tipo de Reserva',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=frame_datos_reserva,
                        values = ['Individual', 'Grupal', 'Corporativa'],#TODO: atarlo a la base de datos
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).grid(row = 1, column = 1, sticky = 'nsew')
        
        #acompañantes
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '👥 Acompañantes',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='cantidad de personas',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     ).grid(row = 1, column = 3, sticky = 'w')
        
        #Habitación específica
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '🏠 Habitación Específica',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 4, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=frame_datos_reserva,
                        values = ['Asignación automática', '101 (Suite)', '102 (Doble)'],#TODO: atarlo a la base de datos
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).grid(row = 1, column = 5, sticky = 'nsew')
        
        #precio por noche
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '💰 Precio por Noche',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 6, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     state='disabled'
                     ).grid(row = 1, column = 7, sticky = 'w')
        
        #requerimientos
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '📝 Notas Especiales',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', padx = 5)
        
        ctk.CTkTextbox(master=frame_datos_reserva,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     ).grid(row = 2, rowspan = 2, column = 1, sticky = 'nsew')
        
        #gastos adicionales
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '💰 Gastos Adicionales',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 2, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     state='disabled'
                     ).grid(row = 2, column = 3, sticky = 'w')
        
        #descuento
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '⬇️ Descuento',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 4, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     state='disabled'
                     ).grid(row = 2, column = 5, sticky = 'w')
        
        #frame de resumen de reserva
        resumen_reserva = ctk.CTkFrame(master=self.tab1, fg_color=AZUL_CLARO, corner_radius=8, width= 500)
        resumen_reserva.pack(anchor = 'w', pady = (8,0))

        ctk.CTkLabel(master=resumen_reserva, 
                     text= '📊 Resumen de Reserva:',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', padx = 18)
        
        ctk.CTkLabel(master=resumen_reserva, 
                     text= 'Complete los datos para ver el resumen',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).pack(anchor = 'w', padx = 18)

        #botones de accion
        btn_frame = ctk.CTkFrame(self.tab1, fg_color="transparent")
        btn_frame.pack(fill = 'x', expand = True, padx = 12, pady = 12)

        btn_disponibilidad = Boton(master=btn_frame,
                           texto='🔍 Verificar Disponibilidad',
                           padx=2,
                           pady=2,
                           fill=None,
                           )
        
        btn_confirmar = Boton(master=btn_frame,
                           texto='✅ Confirmar Reserva',
                           color=VERDE1,
                           hover=VERDE2,
                           padx=2,
                           pady=2,
                           fill=None,
                           )

        btn_limpiar = Boton(master=btn_frame,
                           texto='🔄 Limpiar',
                           color=PRIMARIO,
                           hover=ROJO,
                           padx=2,
                           pady=2,
                           fill=None,
                           )

    def buscar_disponibilidad(self):
        ctk.CTkLabel(master=self.tab2, 
                     text= '🔍 Buscar Disponibilidad de Habitaciones',
                     text_color=PRIMARIO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(pady = 6, padx = 12, anchor = 'w')
        
        #frame para datos de busqueda
        datos_busqueda = ctk.CTkFrame(master=self.tab2, fg_color='transparent')
        datos_busqueda.pack(fill = 'x', expand = True, padx = 0, pady = 0)
        datos_busqueda.columnconfigure(index=(0,1,2,3), weight=1, uniform='m')

        #fecha entrada
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '📅 Fecha de Entrada',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', padx = 5)

        fecha_entrada_entry = CTkDatePicker(master=datos_busqueda)
        fecha_entrada_entry.grid(row = 0, column = 1, sticky = 'nsew')
        fecha_entrada_entry.set_date_format('%d-%m-%Y')
        fecha_entrada_entry.set_localization('es_ES')
        fecha_entrada_entry.set_allow_manual_input(True)

        #Fecha de Salida
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '📅 Fecha de Salida',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx = 5)
        
        fecha_salida_entry = CTkDatePicker(master=datos_busqueda)
        fecha_salida_entry.grid(row = 0, column = 3, sticky = 'nsew')
        fecha_salida_entry.set_date_format('%d-%m-%Y')
        fecha_salida_entry.set_localization('es_ES')
        fecha_salida_entry.set_allow_manual_input(True)

        #Tipo de habitación
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '🏠 Tipo de Habitación',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=datos_busqueda,
                        values = ['Todos los tipos', 'Individual', 'Doble', 'Suite'],#TODO: atarlo a la base de datos
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).grid(row = 1, column = 1, sticky = 'nsew')
        
        #acompañantes
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '👥 Capacidad Mínima',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=datos_busqueda,
                        values = ['Cualquier capacidad', '1 persona', '2 personas', '3 personas', '4+ personas'],
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).grid(row = 1, column = 3, sticky = 'nsew')
        
        #botones de accion
        btn_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        btn_frame.pack(fill = 'x', expand = True, padx = 12)

        btn_disponibilidad = Boton(master=btn_frame,
                           texto='🔍 Buscar Disponibilidad',
                           padx=2,
                           pady=2,
                           fill=None,
                           )
        
        btn_limpiar = Boton(master=btn_frame,
                           texto='🔄 Limpiar',
                           color=PRIMARIO,
                           hover=ROJO,
                           padx=2,
                           pady=2,
                           fill=None,
                           )
        
        # separador
        separador = ctk.CTkFrame(master=self.tab2, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)
        
        ctk.CTkLabel(master=self.tab2, 
                     text= '🏠 Habitaciones Disponibles',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', pady = 12)
        
        #frame para mostrar habitaciones disponibles
        hab_disponibles = ctk.CTkFrame(master = self.tab2, border_color=GRIS_CLARO, border_width=1, corner_radius=10, fg_color=GRIS_CLARO3)
        hab_disponibles.pack(fill = 'both', expand = True, padx = 15, pady = (0,15))
        hab_disponibles.pack_propagate(False)

        #aviso de seleccion
        aviso_selec = ctk.CTkLabel(master=hab_disponibles, 
                     text= '📅\nSeleccione fechas para ver disponibilidad',
                     text_color=MUTE,
                     font = (FUENTE, TAMANO_3)
                     )
        aviso_selec.pack(fill = 'both', expand = True, padx = 20, pady = 20)

    def gestionar_reservas(self):
        #barra búsqueda
        self.barra_busqueda(master=self.tab3)

         # separador
        separador = ctk.CTkFrame(master=self.tab3, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.tabla_reservas(master=self.tab3)

    def historial_reservas(self):
        #barra búsqueda
        self.barra_busqueda(master=self.tab4)

         # separador
        separador = ctk.CTkFrame(master=self.tab4, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.tabla_reservas(master=self.tab4)

    def barra_busqueda(self, master):
        contenedor = ctk.CTkFrame(master=master, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=62)
        contenedor.pack(fill = 'x')
        contenedor.pack_propagate(False)

        ctk.CTkLabel(contenedor, 
                     text='🔍 Buscar:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkEntry(contenedor,
                     placeholder_text='Nombre, tipo o ubicación...',
                     placeholder_text_color=GRIS_CLARO2,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35
                     ).pack(side = 'left', fill = 'x', expand = True, padx = 6)
        
        ctk.CTkLabel(contenedor, 
                     text='Estado:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkComboBox(contenedor,
                        values = ['Todos', 'Disponible', 'Ocupada', 'Sucia', 'Limpiando', 'Mantenimiento', 'Fuera de Servicio'],#TODO: atarlo a la base de datos
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35
                        ).pack(side = 'left', padx = 6)

        btn_buscar = Boton (master=contenedor,
                           texto = 'Buscar', 
                           fill=None, 
                           padx=(12,6))

        btn_limpiar = Boton(master=contenedor,
                            texto='Limpiar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None
                            )
        
    def tabla_reservas(self, master):
        contenedor = ctk.CTkFrame(master = master, fg_color='transparent',border_color='#eee', border_width=1, corner_radius=12)
        contenedor.pack(fill = 'x', expand = True, anchor = 'n')

        contenedor.rowconfigure(index=(0,1), weight=1)
        contenedor.columnconfigure(index=0, weight=1)

        data = [ENCABEZADOS_RESERVAS] + [r for r in RESERVAS()]

        tabla_reservas = CTkTable(master = contenedor, 
                                  row = len(data),
                                  column= len(ENCABEZADOS_RESERVAS),
                                  values=data,
                                  colors=[CLARO, '#eee'],
                                  color_phase='horizontal',
                                  hover_color=MUTE,
                                  border_width=0,
                                  anchor='w',
                                  )
        tabla_reservas.grid(column = 0, row = 0, sticky = 'new', padx = 12, pady = 12)
        tabla_reservas.edit_row(0, font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'))
        tabla_reservas.edit_column(0, width = 65)

        #resaltado segun estado
        colores = {
            'Cancelada': VERDE_CLARO, 
            'Completada': ROJO_CLARO, 
            'Sucia': AMARILLO_CLARO,
        }

        estado_col = ENCABEZADOS_RESERVAS.index('✅ Estado')

        for i, habitacion in enumerate(RESERVAS(), start = 1):
            estado = habitacion[estado_col - 0]
            if estado in colores:
                fg= colores[estado]
                tabla_reservas.edit(row=i, column=estado_col, fg_color=fg)

        btn_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        btn_frame.grid(column = 0, row = 1, sticky = 'new', padx = 12, pady = 12)

        btn_ver = Boton(master=btn_frame,
                           texto='Editar',
                           color=MAMEY,
                           hover=MAMEY2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           )

        btn_fd = Boton(master=btn_frame,
                           texto='Cancelar',
                           color=ROJO,
                           hover=ROJO2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           )
