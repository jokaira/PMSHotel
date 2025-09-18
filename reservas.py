import customtkinter as ctk
from settings import *
from func_clases import *
from datetime import datetime
from tkinter import messagebox

class GestorReservas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #data
        self.cliente_actual = None
        self.fecha_entrada = ctk.StringVar()
        self.fecha_salida = ctk.StringVar()
        self.tipo_habitacion = ctk.StringVar()
        self.acompanantes = ctk.IntVar()
        self.habitacion = ctk.StringVar()
        self.precio = ctk.DoubleVar()
        self.notas = ctk.StringVar()
        self.gastos_adicionales = ctk.DoubleVar()
        self.descuento = ctk.IntVar()
        self.total = 0
        self.noches = 0
        self.combo_map = {}

        #kpi de reservas
        self.kpis = ctk.CTkFrame(master=self, fg_color='transparent', corner_radius=0)
        self.kpis.pack(anchor = 'n',fill = 'x')

        self.kpis.rowconfigure(index=0, weight=0, minsize=109)
        self.kpis.rowconfigure(index=1, weight=0)
        self.kpis.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')
        crear_tarjetas_kpi(master=self.kpis, dict=KPI_RESERVAS())

        #pestañas
        self.contenedor_pestanas = ctk.CTkFrame(master=self, fg_color='transparent')
        self.contenedor_pestanas.pack(anchor = 'n',fill = 'x', pady = (0,10))
        self.boton_pestanas(master=self.contenedor_pestanas)

        self.reservas = ctk.CTkFrame(master=self, fg_color='transparent', border_color=GRIS_CLARO3, corner_radius=10, border_width=0)
        self.reservas.pack(anchor = 'n', fill = 'x')

        self.nueva_reserva()

    def boton_pestanas(self, master):
            self.btn_nueva = ctk.CTkButton(master=master, 
                          text= '➕ Nueva Reserva',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.nueva_reserva,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_nueva.pack(side ='left')

            self.btn_disp = ctk.CTkButton(master=master, 
                          text= '🔍 Buscar Disponibilidad',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.buscar_disponibilidad,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_disp.pack(side ='left', padx = (10,5))

            self.btn_gest = ctk.CTkButton(master=master, 
                          text= '📋 Gestionar Reservas Activas',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.gestionar_reservas,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_gest.pack(side ='left', padx = 5)

            self.btn_historial = ctk.CTkButton(master=master, 
                          text= '📚 Historial',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.historial_reservas,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_historial.pack(side ='left', padx = 5)
    
    def nueva_reserva(self):
        for widget in self.reservas.winfo_children():
            widget.destroy()
        self.btn_nueva.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_disp.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_gest.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_historial.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.reservas.configure(border_width = 1)

        #tracing
        # Tipo de habitación
        self.tipo_habitacion.trace_add("write", lambda *args: mostrar_resumen())

        # Fecha de entrada / salida
        self.fecha_entrada.trace_add("write", lambda *args: mostrar_resumen())
        self.fecha_salida.trace_add("write", lambda *args: mostrar_resumen())

        # Otros campos opcionales
        self.acompanantes.trace_add("write", lambda *args: mostrar_resumen())
        self.habitacion.trace_add("write", lambda *args: mostrar_resumen())
        self.gastos_adicionales.trace_add("write", lambda *args: mostrar_resumen())
        self.descuento.trace_add("write", lambda *args: mostrar_resumen())

        ctk.CTkLabel(master=self.reservas, 
                     text= '📝 Crear Nueva Reserva',
                     text_color=PRIMARIO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(pady = 6, padx = 12, anchor = 'w')
  
        ctk.CTkLabel(master=self.reservas, 
                     text= '👤 Cliente',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).pack(anchor = 'w', pady = 6, padx = 12)
        
        frame_buscador = ctk.CTkFrame(self.reservas, fg_color='transparent')
        frame_buscador.pack(fill = 'x', expand = True)

        busqueda_var = ctk.StringVar()
        
        ctk.CTkEntry(master=frame_buscador,
                     placeholder_text='Buscar cliente por nombre, email o teléfono...',
                     placeholder_text_color=MUTE,
                     textvariable=busqueda_var,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35, width = 335
                     ).pack(side = 'left',pady = 6, padx = (12,5))
        
        frame_busqueda_cliente = ctk.CTkFrame(master=self.master,border_color=GRIS_CLARO2,border_width=2,fg_color='transparent')

        def buscar_cliente():
            busqueda = busqueda_var.get().strip()
            if not busqueda:
                return
            resultado = basedatos.buscar_cliente(busqueda)

            if not resultado:
                return

            frame_busqueda_cliente.place(x = 15, y = 305, anchor = 'nw', relwidth = 0.95)
            frame_busqueda_cliente.lift()

            for cliente in resultado:
                frame = ctk.CTkFrame(master=frame_busqueda_cliente, fg_color='transparent',border_color=GRIS_CLARO2,border_width=1)
                frame.pack(fill = 'x', expand = True)
                frame.bind("<Button-1>", lambda e, c = cliente: seleccionar_cliente(c))
                nombre = ctk.CTkLabel(master=frame, text = f"{cliente[1]} {cliente[2]}", font=(FUENTE,TAMANO_TEXTO_DEFAULT, 'bold'), anchor = 'w')
                nombre.pack(fill = 'both', expand = True, padx = 2, pady = 2)
                nombre.bind("<Button-1>", lambda e, c = cliente: seleccionar_cliente(c))
                contacto = ctk.CTkLabel(master=frame, text = f"📧 {cliente[9]} | 📞 {cliente[8]}", font=(FUENTE,12), anchor = 'w')
                contacto.pack(fill = 'both', expand = True, padx = 2, pady = 2)
                contacto.bind("<Button-1>", lambda e, c = cliente: seleccionar_cliente(c))

        ctk.CTkButton(master = frame_buscador, 
                            text = '🔍 Buscar', 
                            fg_color=AZUL, 
                            hover_color=AZUL2,
                            text_color=BLANCO,font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                            corner_radius=10,
                            command=buscar_cliente
                            ).pack(side = 'left', padx = (0,5))

        #TODO: ver como añadir el modal de nuevo cliente aquí
        ctk.CTkButton(master = frame_buscador, 
                            text = '➕ Nuevo', 
                            fg_color=VERDE1, 
                            hover_color=VERDE2,
                            text_color=BLANCO,font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                            corner_radius=10,
                            ).pack(side = 'left', padx = (0,5))
        
        frame_datos_reserva = ctk.CTkFrame(self.reservas, fg_color='transparent')
        frame_datos_reserva.pack(fill = 'x', expand = True)
        frame_datos_reserva.columnconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='z')

        def seleccionar_cliente(cliente):
            for w in frame_busqueda_cliente.winfo_children():
                w.destroy()
            frame_busqueda_cliente.place_forget()

            if not hasattr(self, 'frame_cliente') or self.frame_cliente.winfo_exists() == 0:
                self.frame_cliente = ctk.CTkFrame(master=frame_datos_reserva, 
                                        height = 40,
                                        fg_color=AZUL_CLARO
                        )
                self.frame_cliente.grid(row = 0, column= 0, columnspan = 2, sticky = 'ew', padx = 5)

            cliente_seleccionado = ctk.CTkFrame(master=self.frame_cliente, height = 81, fg_color='#fcfcfc', border_color=GRIS_CLARO2, border_width=1, corner_radius=10)
            cliente_seleccionado.pack(fill = 'both', expand = True, padx = 8, pady = 8)

            nombre_cliente = f"Cliente seleccionado: {cliente[1]} {cliente[2]}"
            contacto_cliente = f"📧 {cliente[9]} | 📞 {cliente[8]}"
            ctk.CTkLabel(master=cliente_seleccionado, text=nombre_cliente, text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT)).pack(anchor = 'w', padx = 5, pady = (5,0))
            ctk.CTkLabel(master=cliente_seleccionado, text=contacto_cliente, text_color=OSCURO, font=(FUENTE, 12)).pack(anchor = 'w', padx = 5, pady = (0,5))

            ctk.CTkButton(master=cliente_seleccionado, text='Cambiar', text_color=CLARO, font=(FUENTE, 12), fg_color=PRIMARIO, hover_color=ROJO, width=50, command=lambda f = self.frame_cliente: limpiar_cliente(f)).place(relx = 0.98, rely = 0.5, anchor = 'e')

            self.cliente_actual = cliente
            mostrar_resumen()

        def limpiar_cliente(frame):
            for w in frame.winfo_children():
                w.destroy()
            frame.grid_forget()

            self.cliente_actual = None

        #Fecha de Entrada
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '📅 Fecha de Entrada',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx = 5)

        fecha_entrada_entry = CTkDatePicker(master=frame_datos_reserva)
        fecha_entrada_entry.date_entry.configure(textvariable = self.fecha_entrada)
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
        fecha_salida_entry.date_entry.configure(textvariable = self.fecha_salida)
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
        
        #obtener tipos de habitacion en la base de datos
        tipos_hab = [row[1] for row in basedatos.obtener_tipos_habitaciones()]
                
        #actualizar cada vez q cambia el tipo
        def actualizar_habitaciones(opcion):
            habitaciones = basedatos.hab_por_tipo(opcion.strip())
            if habitaciones:
                self.combo_map = {f"{hab[1]}, {hab[4]}": str(hab[0]) for hab in habitaciones}
                #rellenar combobox
                valores = list(self.combo_map.keys())
                combo_habitaciones.configure(values = valores)


                precio = basedatos.precio_por_tipo(opcion.strip())
                if precio:
                    self.precio.set(precio)
            else:
                combo_habitaciones.configure(values = [''])
                self.precio.set(0.0) 
                self.combo_map = {}

        ctk.CTkComboBox(master=frame_datos_reserva,
                        values = tipos_hab,
                        variable= self.tipo_habitacion,
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
                        border_width=1, height=35,
                        command=actualizar_habitaciones
                        ).grid(row = 0, column = 7, sticky = 'ew')
        
        #acompañantes
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '👥 Acompañantes',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='cantidad de personas',
                     placeholder_text_color=MUTE,
                     textvariable=self.acompanantes,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     ).grid(row = 1, column = 1, sticky = 'w')
        
        #Habitación específica
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '🏠 Habitación Específica',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx = 5)
        
        combo_habitaciones = ctk.CTkComboBox(master=frame_datos_reserva,
                        corner_radius=8,
                        variable=self.habitacion,
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
                        )
        combo_habitaciones.grid(row = 1, column = 3, sticky = 'ew')
        
        #precio por noche
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '💰 Precio por Noche ($)',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 4, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     textvariable=self.precio,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     state='disabled'
                     ).grid(row = 1, column = 5, sticky = 'w')
        
        #requerimientos
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '📝 Notas Especiales',
                                          text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     textvariable=self.notas
                     ).grid(row = 2, rowspan = 2, column = 1, sticky = 'w')
        
        #gastos adicionales
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '💰 Gastos Adicionales ($)',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 2, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     textvariable=self.gastos_adicionales,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     ).grid(row = 2, column = 3, sticky = 'w')
        
        #descuento
        ctk.CTkLabel(master=frame_datos_reserva, 
                     text= '⬇️ Descuento (%)',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 4, sticky = 'w', padx = 5)
        
        ctk.CTkEntry(master=frame_datos_reserva,
                     textvariable=self.descuento,
                     placeholder_text='0.00',
                     placeholder_text_color=MUTE,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35,
                     ).grid(row = 2, column = 5, sticky = 'w')
        
        #frame de resumen de reserva
        resumen_reserva = ctk.CTkFrame(master=self.reservas, fg_color=AZUL_CLARO, corner_radius=8, width= 500)
        resumen_reserva.pack(anchor = 'w', pady = (8,0))

        ctk.CTkLabel(master=resumen_reserva, 
                     text= '📊 Resumen de Reserva:',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', padx = 18)
        
        completar = ctk.CTkLabel(master=resumen_reserva, 
                     text= 'Complete los datos para ver el resumen',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     )
        completar.pack(anchor = 'w', padx = 18)

        def mostrar_resumen():
            fecha_entrada = self.fecha_entrada.get().strip()
            fecha_salida = self.fecha_salida.get().strip()
            tipo_hab = self.tipo_habitacion.get().strip()
            hab = self.habitacion.get().strip()
            try:
                acompanantes = int(self.acompanantes.get())
            except (tk.TclError, ValueError):
                acompanantes = 0

            formato = "%d-%m-%Y"
            try:
                if (datetime.strptime(fecha_salida, formato) - datetime.strptime(fecha_entrada, formato)).days <= 0:
                        messagebox.showerror("Error","La fecha de salida debe ser posterior a la fecha de entrada")
                        self.fecha_salida.set("")
                        return
            except:
                pass

            if not (fecha_entrada and fecha_salida and tipo_hab):
                completar.pack(anchor = 'w', padx = 18)
                return
                           
            completar.pack_forget()

            # Crear contenedor solo si no existe aún
            if not hasattr(self, 'contenedor_resumen') or self.contenedor_resumen.winfo_exists() == 0:
                self.contenedor_resumen = ctk.CTkFrame(
                    master=resumen_reserva,
                    fg_color=CLARO,
                    border_color=GRIS_CLARO2,
                    border_width=1,
                    corner_radius=10)
                self.contenedor_resumen.pack(fill='both', expand=True, padx=12, pady=12)
            
            # Limpiar contenido previo
            for widget in self.contenedor_resumen.winfo_children():
                widget.destroy()
            
            # Calcular cantidad de días
            formato = "%d-%m-%Y"
            try:
                entrada_dt = datetime.strptime(fecha_entrada, formato)
                salida_dt = datetime.strptime(fecha_salida, formato)
                self.noches = (salida_dt - entrada_dt).days
                if self.noches < 0:
                    self.noches = 0
            except:
                self.noches = 0

            # Calcular precio total
            try:
                precio_por_noche = float(self.precio.get() or 0)
                gastos_adicionales = float(self.gastos_adicionales.get() or 0)
                descuento = int(self.descuento.get() or 0)
                self.total = (precio_por_noche * self.noches) * (1 - descuento/100) + gastos_adicionales
            except:
                self.total = 0.0

            if self.cliente_actual is not None:
                cliente = f"{self.cliente_actual[1]} {self.cliente_actual[2]}"
            else:
                cliente = "No seleccionado"

            # Mostrar resumen
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Cliente: {cliente}", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Tipo de habitación: {tipo_hab}", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Fechas: {fecha_entrada} al {fecha_salida} ({self.noches} noches)", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Total personas: {acompanantes + 1} ({acompanantes} acompañantes)", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Precio por noche: ${precio_por_noche:.2f}", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Descuento: {descuento}%", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Gastos adicionales: ${gastos_adicionales:.2f}", anchor='w').pack(fill='x', padx=5)
            ctk.CTkLabel(self.contenedor_resumen, text_color=OSCURO,text=f"Total: ${self.total:.2f}", anchor='w', font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')).pack(fill='x', padx=5)

            # TODO: añadir validador de disponibilidad de habitación

        #botones de accion
        btn_frame = ctk.CTkFrame(self.reservas, fg_color="transparent")
        btn_frame.pack(fill = 'x', expand = True, padx = 12, pady = 12)

        def mostrar_disponibilidad():
            fecha_entrada = self.fecha_entrada.get().strip()
            fecha_salida = self.fecha_salida.get().strip()
            tipo_hab = self.tipo_habitacion.get().strip()

            if not (fecha_entrada and fecha_salida and tipo_hab):
                return

            hab_disp = basedatos.hab_disponibles(fecha_entrada=fecha_entrada, fecha_salida=fecha_salida)
       
            cant_habitaciones = 0
            string_disponibles = ""

            for habitacion in hab_disp:
                if habitacion[1] != tipo_hab:
                    continue
                cant_habitaciones += 1
                string_disponibles += f"Habitación {habitacion[0]} en el {habitacion[2]}\n"


            if cant_habitaciones == 0:
                messagebox.showinfo("Habitaciones disponibles", "No hay habitaciones disponibles para esas fechas")
                self.habitacion.set("")
                return
            messagebox.showinfo("Habitaciones disponibles",f"{cant_habitaciones} habitaciones disponibles:\n {string_disponibles}")
            

        def limpiar():
            if hasattr(self,"contenedor_resumen"):
                self.contenedor_resumen.destroy()

            completar.pack(anchor = 'w', padx = 18)

            if hasattr(self,"frame_cliente"):
                self.frame_cliente.destroy()

            self.cliente_actual = None
            self.fecha_entrada.set("")
            self.fecha_salida.set("")
            self.tipo_habitacion.set("")
            self.acompanantes.set(0)
            self.habitacion.set("")
            self.precio.set(0.00)
            self.notas.set("")
            self.gastos_adicionales.set(0.00)
            self.descuento.set(0)
        
        def modal_reservas(tipo):
            titulo_ventana = ""
            titulo_modal = ""
            match tipo:
                case "pago":
                    titulo_ventana = "Confirmar Reserva"
                    titulo_modal = "💳 Registrar Pago - Nueva Reserva"

            dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
            dialogo.title(titulo_ventana)
            dialogo.geometry("720x380")
            dialogo.resizable(False,False)
            dialogo.transient(self)
            dialogo.grab_set()
            
            #titulo
            ctk.CTkLabel(dialogo, 
                        text= titulo_modal, 
                        text_color=OSCURO, 
                        font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                        ).pack(anchor = 'w', pady = (16,0), padx = 16)
            
            ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

            match tipo:
                case "pago":
                    self.crear_formulario_pago(master = dialogo)

        btn_disponibilidad = Boton(master=btn_frame,
                           texto='🔍 Verificar Disponibilidad',
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=mostrar_disponibilidad
                           )
        
        btn_confirmar = Boton(master=btn_frame,
                           texto='✅ Confirmar Reserva',
                           color=VERDE1,
                           hover=VERDE2,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=lambda:modal_reservas(tipo="pago")
                           )

        btn_limpiar = Boton(master=btn_frame,
                           texto='🔄 Limpiar',
                           color=PRIMARIO,
                           hover=ROJO,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=limpiar
                           )

    def crear_formulario_pago(self, master): #TODO: readecuar al nuevo módulo
        if not self.cliente_actual:
            messagebox.showerror("Error", "Debe de seleccionar un cliente")
            master.destroy()
            return

        habitacion = self.habitacion.get().strip() #TODO: agregar validación para verificar si la habitacion está disponible para reserva
        tipo_hab = self.tipo_habitacion.get().strip()
        nombre_cliente = str(self.cliente_actual[1] + " " +self.cliente_actual[2])
        id_cliente = self.cliente_actual[0]
        email_cliente = self.cliente_actual[9]
        fecha_entrada = datetime.strftime(datetime.strptime(self.fecha_entrada.get().strip(),'%d-%m-%Y'), '%Y-%m-%d')
        fecha_salida = datetime.strftime(datetime.strptime(self.fecha_salida.get().strip(),'%d-%m-%Y'), '%Y-%m-%d')
        pago_total = self.total

        if not habitacion or not fecha_entrada or not fecha_salida:
            messagebox.showerror("Error", "Debe de completar todos los datos obligatorios para la reserva")
            return

        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        #variables de los campos
        metodo_pago = ctk.StringVar()
        comprobante_pago = ctk.StringVar()
        notas_pago = ctk.StringVar()
                
        # #letrero de campos obligatorios
        ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios").place(relx = 0.95, rely = 0.95, anchor = 'se')

        datos_reserva = ctk.CTkFrame(master=frame_formulario, corner_radius=10, border_color=GRIS_CLARO2, border_width=1, fg_color=GRIS_CLARO)
        datos_reserva.pack(fill = 'x', anchor = 'n')

        ctk.CTkLabel(master=datos_reserva, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Cliente: {nombre_cliente}", anchor='w').pack(fill='x',expand = True, padx=5)
        ctk.CTkLabel(master=datos_reserva, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Habitación: {habitacion} ({tipo_hab})", anchor='w').pack(fill='x',expand = True, padx=5)
        ctk.CTkLabel(master=datos_reserva, text_color=OSCURO, font = (FUENTE, TAMANO_TEXTO_DEFAULT),text=f"Fechas: {fecha_entrada} al {fecha_salida}", anchor='w').pack(fill='x',expand = True, padx=5)
        ctk.CTkLabel(master=datos_reserva, text_color=OSCURO,text=f"Total: ${pago_total:.2f}", anchor='w', font=(FUENTE, TAMANO_TEXTO_DEFAULT)).pack(fill='x',expand = True, padx=5)

        campos_pago = ctk.CTkFrame(master=frame_formulario, corner_radius=10, fg_color='transparent')
        campos_pago.pack(fill = 'x', anchor = 'n', pady = 8)

        #método de pago
        ctk.CTkLabel(master=campos_pago,
                     text='💳 Método de Pago*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkComboBox(master=campos_pago,
                        variable=metodo_pago,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=['Efectivo', 'Tarjeta', 'Transferencia', 'Cheque']
                        ).grid(row=0, column=1, sticky = 'nsew', pady= (0,12))
        
        #comprobante de pago
        ctk.CTkLabel(master=campos_pago,
                     text='📝 Número de Comprobante*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx= (12,0), pady = (0,12))
        ctk.CTkEntry(master=campos_pago,
                     textvariable=comprobante_pago,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 3, sticky = 'nsew', pady = (0,12))
        
        #notas de pago
        ctk.CTkLabel(master=campos_pago,
                     text='📝 Notas del Pago',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkEntry(master=campos_pago,
                     textvariable=comprobante_pago,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 1, sticky = 'nsew', pady = (0,12))

        def guardar():
            #datos a guardar en formulario
            #primero guardo el pago
            datos_pago = [
                'reserva',
                f'Pago reserva habitación {habitacion} - {nombre_cliente} - {self.noches} noches',
                pago_total,
                metodo_pago.get().strip().lower(),
                comprobante_pago.get().strip(),
                notas_pago.get().strip()
            ]

            if not datos_pago[3] or not datos_pago[4]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje_pago, id_pago = basedatos.registrar_pago(datos=datos_pago)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje_pago)
                return

            #ahora guardo la reserva
            #TODO: Modificar tabla de reservas para poder registrar el ID de pago

            master.destroy()


        btn_frame = ctk.CTkFrame(master=frame_formulario, fg_color='transparent')
        btn_frame.pack(fill ='x', expand = True)

        btn_frame.columnconfigure(index=(0,1,2,3,4,5,6,7), weight = 1, uniform= 'z')

        #boton cancelar
        ctk.CTkButton(master = btn_frame,
                      text='Cancelar',
                      fg_color=PRIMARIO,
                      hover_color=ROJO,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=master.destroy,
                        ).grid(row = 6, column = 0, pady = 12)
        
        #boton confirmar reserva
        ctk.CTkButton(master = btn_frame,
                      text='✅ Pagar y Confirmar Reserva',
                      fg_color=VERDE1,
                      hover_color=VERDE2,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command="guardar",
                        ).grid(row = 6, column = 1, columnspan = 4,pady = 12)

    def buscar_disponibilidad(self):
        for widget in self.reservas.winfo_children():
            widget.destroy()

        self.btn_disp.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 

        self.btn_nueva.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_gest.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_historial.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.reservas.configure(border_width = 1)

        ctk.CTkLabel(master=self.reservas, 
                     text= '🔍 Buscar Disponibilidad de Habitaciones',
                     text_color=PRIMARIO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(pady = 6, padx = 12, anchor = 'w')
        
        #frame para datos de busqueda
        datos_busqueda = ctk.CTkFrame(master=self.reservas, fg_color='transparent')
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
        btn_frame = ctk.CTkFrame(self.reservas, fg_color="transparent")
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
        separador = ctk.CTkFrame(master=self.reservas, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)
        
        ctk.CTkLabel(master=self.reservas, 
                     text= '🏠 Habitaciones Disponibles',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', pady = 12)
        
        #frame para mostrar habitaciones disponibles
        hab_disponibles = ctk.CTkFrame(master = self.reservas, border_color=GRIS_CLARO, border_width=1, corner_radius=10, fg_color=GRIS_CLARO3)
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
        for widget in self.reservas.winfo_children():
            widget.destroy()

        self.btn_gest.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 

        self.btn_nueva.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_disp.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_historial.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.reservas.configure(border_width = 0)

        #barra búsqueda
        self.barra_busqueda(master=self.reservas)

         # separador
        separador = ctk.CTkFrame(master=self.reservas, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.tabla_reservas(master=self.reservas)

    def historial_reservas(self):
        for widget in self.reservas.winfo_children():
            widget.destroy()

        self.btn_historial.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 

        self.btn_nueva.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_disp.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_gest.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.reservas.configure(border_width = 0)

        #barra búsqueda
        self.barra_busqueda(master=self.reservas)

         # separador
        separador = ctk.CTkFrame(master=self.reservas, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.tabla_reservas(master=self.reservas)

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
