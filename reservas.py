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
        self.selec = []
        self.busqueda_var = ctk.StringVar()
        self.filtro_estado = ctk.StringVar(value = 'Todos')

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
        try:
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
        except Exception:
            return

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
                try:
                    completar.pack(anchor = 'w', padx = 18)
                    return
                except:
                    return
            try:
                completar.pack_forget()
            except:
                return

            # Crear contenedor solo si no existe aún
            if not hasattr(self, 'contenedor_resumen') or self.contenedor_resumen.winfo_exists() == 0:
                try:
                    self.contenedor_resumen = ctk.CTkFrame(
                        master=resumen_reserva,
                        fg_color=CLARO,
                        border_color=GRIS_CLARO2,
                        border_width=1,
                        corner_radius=10)
                    self.contenedor_resumen.pack(fill='both', expand=True, padx=12, pady=12)
                except Exception:
                    return
                
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

        #botones de accion
        btn_frame = ctk.CTkFrame(self.reservas, fg_color="transparent")
        btn_frame.pack(fill = 'x', expand = True, padx = 12, pady = 12)

        def mostrar_disponibilidad():
            fecha_entrada = self.fecha_entrada.get().strip()
            fecha_salida = self.fecha_salida.get().strip()
            tipo_hab = self.tipo_habitacion.get().strip()

            if not (fecha_entrada and fecha_salida and tipo_hab):
                return

            try:
                fe_ini_dt = datetime.strptime(fecha_entrada, '%d-%m-%Y')
                fe_fin_dt = datetime.strptime(fecha_salida, '%d-%m-%Y')
                fe_ini_iso = fe_ini_dt.date().isoformat()
                fe_fin_iso = fe_fin_dt.date().isoformat()
            except Exception as e:
                print("DEBUG: error parseando fechas:", fecha_entrada, fecha_salida, e)
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-YYYY")
                return

            print("DEBUG llamar hab_disponibles con (ISO):", fe_ini_iso, fe_fin_iso, "tipo:", tipo_hab)
            hab_disp = basedatos.hab_disponibles(fecha_entrada=fe_ini_iso, fecha_salida=fe_fin_iso, tipo=tipo_hab)

       
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
                           metodo=self.guardar_reserva
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

    def modal_reservas(self, tipo):
            titulo_ventana = ""
            titulo_modal = ""
            match tipo:
                case "pago":
                    titulo_ventana = "Confirmar Reserva"
                    titulo_modal = "💳 Registrar Pago - Nueva Reserva"
                case "ver":
                    titulo_ventana = "Ver Reserva"
                    titulo_modal = "📋 Detalle de Reserva"

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
                case "ver":
                    self.ver_reserva(master=dialogo)

    def guardar_reserva(self):
            if not self.cliente_actual:
                messagebox.showerror("Error", "Debe de seleccionar un cliente")
                return

            habitacion = self.habitacion.get().strip() 
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
            
            datos_reserva = [
                    habitacion[:3],
                    tipo_hab,
                    id_cliente,
                    nombre_cliente,
                    email_cliente,
                    fecha_entrada,
                    fecha_salida,
                    self.acompanantes.get() + 1,
                    0,
                    pago_total,
                    self.notas.get().strip()
                ]

            print("DEBUG datos_reserva len:", len(datos_reserva))
            print("DEBUG datos_reserva:", datos_reserva)

            disponibles = []
            for habitacion in basedatos.hab_disponibles(fecha_entrada=datos_reserva[5], fecha_salida=datos_reserva[6], tipo=datos_reserva[1]):
                disponibles.append(habitacion[0])

            print(f"Habitaciones disponibles: {disponibles}")

            if datos_reserva[0] not in disponibles:
                messagebox.showerror("Habitación no disponible",f"La habitación {datos_reserva[0]} no está disponible en estas fechas")
                return

            reserva_guardada, mensaje_reserva = basedatos.guardar_reserva(tipo="agregar",datos=datos_reserva)

            if not reserva_guardada:
                messagebox.showerror("Error", mensaje_reserva)
                return
            
            messagebox.showinfo("Reserva guardada", "La reserva fue guardada exitosamente")
            return



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
        fecha_entrada_entry.date_entry.configure(textvariable = self.fecha_entrada)
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
        fecha_salida_entry.date_entry.configure(textvariable = self.fecha_salida)
        fecha_salida_entry.set_date_format('%d-%m-%Y')
        fecha_salida_entry.set_localization('es_ES')
        fecha_salida_entry.set_allow_manual_input(True)

        #Tipo de habitación
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '🏠 Tipo de Habitación',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', padx = 5)
        
        valores_tipos_hab = ['Todos'] + [row[1] for row in basedatos.obtener_tipos_habitaciones()]
        self.tipo_habitacion.set(valores_tipos_hab[0])
        
        ctk.CTkComboBox(master=datos_busqueda,
                        values = valores_tipos_hab,
                        variable=self.tipo_habitacion,
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
        
        #capacidad minima
        self.capacidad = ctk.StringVar(value='Cualquiera')
        ctk.CTkLabel(master=datos_busqueda, 
                     text= '👥 Capacidad Mínima',
                     text_color=OSCURO,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx = 5)
        
        ctk.CTkComboBox(master=datos_busqueda,
                        values = ['Cualquiera', '1 persona', '2 personas', '3 personas', '4+ personas'],
                        variable=self.capacidad,
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
        
        def mostrar_disponibilidad(): 
            fecha_entrada = self.fecha_entrada.get().strip()
            fecha_salida = self.fecha_salida.get().strip()
            tipo_hab = self.tipo_habitacion.get().strip()
            capacidad = int(self.capacidad.get().strip()[0]) if self.capacidad.get().strip() != "Cualquiera" else None

            if not (fecha_entrada and fecha_salida):
                return

            try:
                fe_ini_dt = datetime.strptime(fecha_entrada, '%d-%m-%Y')
                fe_fin_dt = datetime.strptime(fecha_salida, '%d-%m-%Y')
                fe_ini_iso = fe_ini_dt.date().isoformat()
                fe_fin_iso = fe_fin_dt.date().isoformat()
            except Exception as e:
                print("DEBUG: error parseando fechas:", fecha_entrada, fecha_salida, e)
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-YYYY")
                return

            print("DEBUG llamar hab_disponibles con (ISO):", fe_ini_iso, fe_fin_iso, "tipo:", tipo_hab)
            hab_disp = basedatos.hab_disponibles(fecha_entrada=fe_ini_iso, fecha_salida=fe_fin_iso, tipo=tipo_hab)


            cantidad=len(hab_disp)

            if cantidad == 0:
                aviso_selec.configure(text = "No hay habitaciones disponibles en esas fechas")
                return
            
            for w in hab_disponibles.winfo_children():
                try:
                    w.pack_forget()
                    w.place_forget()
                    w.grid_forget()
                except:
                    pass

            frame_cantidad = ctk.CTkFrame(master=hab_disponibles, corner_radius=10, fg_color='transparent', border_color=GRIS_CLARO, border_width=1)
            frame_cantidad.pack(fill = 'x', anchor = 'n', padx = 12, pady = 12)

            ctk.CTkLabel(master=frame_cantidad,
                         text=f"✅ {cantidad} habitaciones disponibles",
                         font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'),
                         text_color=OSCURO
                         ).pack(anchor = 'w',  padx = 15, pady = (2,0))
            
            ctk.CTkLabel(master=frame_cantidad,
                         text=f"Para el periodo {fecha_entrada} al {fecha_salida}",
                         font=(FUENTE, 12),
                         text_color=OSCURO
                         ).pack(anchor = 'w', padx = 15, pady = (0,2))
            
            tarjetas_habitaciones = ctk.CTkFrame(master=hab_disponibles, fg_color='transparent', corner_radius=0)
            tarjetas_habitaciones.pack(fill = 'x', expand = True, padx = 12, pady = 5)

            for habitacion in hab_disp:
                hab_card = ctk.CTkFrame(master=tarjetas_habitaciones, fg_color=BLANCO, border_color=GRIS_CLARO3, border_width=1,corner_radius=12)
                hab_card.pack(side = 'left', padx = (0,15), pady = 0)

                ctk.CTkLabel(master=hab_card,
                            text=f"Hab. {habitacion[0]}",
                            font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'),
                            text_color=OSCURO
                            ).pack(anchor = 'w',  padx = 15)
                ctk.CTkLabel(master=hab_card,
                            text=f"{habitacion[1]} • {habitacion[3]} personas",
                            font=(FUENTE, 12),
                            text_color=OSCURO
                            ).pack(anchor = 'w',  padx = 15)
                ctk.CTkLabel(master=hab_card,
                            text=f"{habitacion[2]}",
                            font=(FUENTE, 12),
                            text_color=OSCURO
                            ).pack(anchor = 'w',  padx = 15)          

        def limpiar():
            self.fecha_entrada.set("")
            self.fecha_salida.set("")
            self.tipo_habitacion.set("Todos")
            self.capacidad.set("Cualquiera")

            for w in hab_disponibles.winfo_children():
                try:
                    w.pack_forget()
                    w.place_forget()
                    w.grid_forget()
                except:
                    pass

            aviso_selec.configure(text = '📅\nSeleccione fechas para ver disponibilidad')
            aviso_selec.pack(fill = 'both', expand = True, padx = 20, pady = 20)

        #botones de accion
        btn_frame = ctk.CTkFrame(self.reservas, fg_color="transparent")
        btn_frame.pack(fill = 'x', expand = True, padx = 12)

        btn_disponibilidad = Boton(master=btn_frame,
                           texto='🔍 Buscar Disponibilidad',
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=mostrar_disponibilidad
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
        self.barra_busqueda(master=self.reservas, tipo_tabla='actual')

         # separador
        separador = ctk.CTkFrame(master=self.reservas, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.contenedor_tabla = ctk.CTkFrame(self.reservas, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = 12)

        reservas = RESERVAS()
        data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Pendiente', 'En curso', 'checked-in')]
        self.tabla_reservas(data=data_tabla)

        btn_frame = ctk.CTkFrame(self.contenedor_tabla, fg_color="transparent")
        btn_frame.pack(fill = 'x', anchor = 'n', padx = 12, pady = 12)

        btn_ver = Boton(master=btn_frame,
                           texto='Ver reserva',
                           color=MAMEY,
                           hover=MAMEY2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo= lambda: self.modal_reservas("ver")
                           )

        btn_cancelar = Boton(master=btn_frame,
                           texto='Cancelar',
                           color=ROJO,
                           hover=ROJO2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=self.cancelar_reserva
                           )

    def historial_reservas(self):
        for widget in self.reservas.winfo_children():
            widget.destroy()

        self.btn_historial.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 

        self.btn_nueva.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_disp.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.btn_gest.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.reservas.configure(border_width = 0)

        #barra búsqueda
        self.barra_busqueda(master=self.reservas, tipo_tabla="historial")

         # separador
        separador = ctk.CTkFrame(master=self.reservas, height=2, fg_color=GRIS_CLARO3)
        separador.pack(fill="x", pady=10)

        #tabla de reservas
        self.contenedor_tabla = ctk.CTkFrame(self.reservas, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = 12)
        
        reservas = RESERVAS()
        data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Cancelada', 'Completada')]
        self.tabla_reservas(data=data_tabla)

        btn_frame = ctk.CTkFrame(self.contenedor_tabla, fg_color="transparent")
        btn_frame.pack(fill = 'x', anchor = 'n', padx = 12, pady = 12)

        btn_ver = Boton(master=btn_frame,
                           texto='Ver reserva',
                           color=MAMEY,
                           hover=MAMEY2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo= lambda: self.modal_reservas("ver")
                           )

    def barra_busqueda(self, master, tipo_tabla):
        contenedor = ctk.CTkFrame(master=master, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=62)
        contenedor.pack(fill = 'x')
        contenedor.pack_propagate(False)

        ctk.CTkLabel(contenedor, 
                     text='🔍 Buscar:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkEntry(contenedor,
                     textvariable=self.busqueda_var,
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
                        values = ['Todos', 'Pendiente', 'En curso', 'Completada', 'Cancelada'],
                        variable=self.filtro_estado,
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
                           padx=(12,6),
                           metodo= lambda: self.buscar(tipo_tabla=tipo_tabla)
                           )

        btn_limpiar = Boton(master=contenedor,
                            texto='Limpiar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None,
                            metodo= lambda: self.limpiar_busqueda(tipo_tabla=tipo_tabla)
                            )

    def seleccion_reserva(self, fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w, _ in self.celdas[fila]]
        self.selec = valores
        print(self.selec)

        #resaltado
        for f, fila_widgets in enumerate(self.celdas):
            for w, es_badge in fila_widgets:
                if es_badge:
                    continue
    
                if f == fila:
                    w.configure(fg_color = AZUL_CLARO)
                else:
                    if f == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    elif f % 2 == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    else:
                        default_bg = GRIS_CLARO4
                        default_text = OSCURO

                    w.configure(fg_color=default_bg, text_color=default_text)

    def tabla_reservas(self, data):
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

        #resaltado segun estado
        colores = {
                    'Completada': VERDE1, 
                    'En curso': AZUL, 
                    'Pendiente': MAMEY, 
                    'Cancelada': ROJO,
                    'checked-in': AZUL
                  }

        self.celdas = []
        for f, fila in enumerate(data):
            fila_widgets = []
            for c, texto in enumerate(fila):
                  #coloreado de las lineas
                  if f == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                  elif f % 2 == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, 12)
                  else:
                    bg = GRIS_CLARO4
                    fg = OSCURO
                    font = (FUENTE, 12)

                  if c == 5 and f != 0:
                    try:
                          texto = datetime.strftime(datetime.strptime(texto, '%Y-%m-%d'),'%d-%m-%Y')
                    except ValueError:
                        pass
                
                  if c == 4 and f != 0:
                    try:
                          texto = datetime.strftime(datetime.strptime(texto, '%Y-%m-%d'),'%d-%m-%Y')
                    except ValueError:
                        pass

                  #resaltado de estado con "pilas"
                  if texto in colores:
                      cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                      cont_pila.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                      pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height = 28)
                      pila.pack(fill = 'y')

                      lbl = ctk.CTkLabel(master=pila, text='EN CURSO' if texto == 'checked-in' else texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                      lbl.pack(expand = True, padx = 8, pady = 2)

                      if f > 0:
                        lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_reserva(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_reserva(fila))
                    widget_celda = (lbl, False)
                  
                  frame.grid_columnconfigure(c, weight=1)

                  #borde encabezado
                  if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column = c, sticky = 'ew')
                    borde.grid_propagate(False)
                    borde.configure(height = 2)

                  #bind capturando fila
                  
                  fila_widgets.append(widget_celda)
            self.celdas.append(fila_widgets) 

    def buscar(self, tipo_tabla):
        busqueda = self.busqueda_var.get().strip()
        filtro_estado = self.filtro_estado.get().strip()
        if not busqueda:
            reservas = RESERVAS()
            if tipo_tabla == "actual":
                data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Pendiente', 'En curso')]
                self.tabla_reservas(data=data_tabla)
            else:
                data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Cancelada', 'Completada')]
                self.tabla_reservas(data=data_tabla)

        resultado = basedatos.buscar_reserva(texto=busqueda, estado=filtro_estado)
        if tipo_tabla=="actual":
            data = [ENCABEZADOS_RESERVAS] + [r for r in resultado if r[8] in ('Pendiente', 'En curso')]
        else:
            data = [ENCABEZADOS_RESERVAS] + [r for r in resultado if r[8] in ('Cancelada', 'Completada')]
        self.tabla_reservas(data=data)
    
    def limpiar_busqueda(self, tipo_tabla):
        self.busqueda_var.set('')
        self.filtro_estado.set('Todos')

        reservas = RESERVAS()
        if tipo_tabla == "actual":
            data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Pendiente', 'En curso')]
            self.tabla_reservas(data=data_tabla)
        else:
            data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Cancelada', 'Completada')]
            self.tabla_reservas(data=data_tabla)

    def ver_reserva(self, master):
        if not self.selec:
            messagebox.showerror("Error", "Debe seleccionar una reserva")
            master.destroy()
            return
        
        reserva = basedatos.ver_reserva(id=self.selec[0])
        descripcion = ['ID de Reserva', 'Número de Habitación', 'Tipo de Habitación', 'Nombre del Cliente', 'Correo del Cliente', 'Fecha de Entrada', 'Fecha de Salida', 'Total de Huéspedes', 'Monto Pagado', 'Estado', 'Fecha de reserva', 'Notas adicionales']

        contenedor = ctk.CTkFrame(master=master, fg_color=GRIS_CLARO4)
        contenedor.pack(fill = 'both', expand = True, padx = 16, pady = (0,10))
        
        contenedor.columnconfigure(index=(0,1,2,3), weight = 1, uniform= 'k')

        for i, (desc, valor) in enumerate(zip(descripcion, reserva)):
            if i == len(descripcion) - 1:
                fila = (i // 2) + 1  # Nueva fila al final
                label_desc = ctk.CTkLabel(contenedor, text=desc + ": ", text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'))
                label_val = ctk.CTkLabel(contenedor, text=str(valor), text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT))
                label_desc.grid(row=fila, column=0, padx=(8,2), pady=4, sticky="e")
                label_val.grid(row=fila, column=1, columnspan=3, padx=(2,8), pady=4, sticky="w")
            else:
                fila = i // 2
                columna = (i % 2) * 2  # Multiplica por 2 porque cada valor ocupa dos columnas (label y valor)
                label_desc = ctk.CTkLabel(contenedor, text=desc + ": ", text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'))
                label_val = ctk.CTkLabel(contenedor, text=str(valor), text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT))
                label_desc.grid(row=fila, column=columna, padx=(8,2), pady=4, sticky="e")
                label_val.grid(row=fila, column=columna+1, padx=(2,8), pady=4, sticky="w")

    def cancelar_reserva(self):
        if not self.selec:
            messagebox.showerror("Error", "Debe seleccionar una reserva")
            return
        
        id = self.selec[0]
        if self.selec[8].lower() != 'pendiente':
            messagebox.showerror("Error", "No es posible cancelar esta reserva")
            return
        
        confirmacion = messagebox.askyesno("Cancelar", f"¿Está seguro que desea cancelar esta reserva?\n Reserva No. {id} para el cliente {self.selec[2]} en la habitación {self.selec[1]}\nNOTA: El cliente no obtendrá reembolso.")

        if confirmacion:
            razon_cancelacion = ctk.CTkInputDialog(title="Razón", text="Digite el motivo de la cancelación:")
            fue_cancelada, mensaje = basedatos.modificar_estado_reserva(estado='Cancelada', id=id, motivo = razon_cancelacion.get_input())
            if not fue_cancelada:
                messagebox.showerror("Error", mensaje)
                return
            messagebox.showinfo("Reserva cancelada", "La reserva fue cancelada exitosamente")

        #actualizar tabla
        from settings import RESERVAS
        reservas = RESERVAS()
        data_tabla = [ENCABEZADOS_RESERVAS] + [r for r in reservas if r[8] in ('Pendiente', 'En curso')]
        self.tabla_reservas(data=data_tabla)
