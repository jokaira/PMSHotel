import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, date
import requests
import sqlite3
import os
from settings import *
from func_clases import Boton, crear_tarjetas_kpi
from settings import EARLY_CHECKOUT_PENALTY_PERCENT, KPI_FRONTDESK
from basedatos import (validar_fecha,
    buscar_reserva_frontdesk as buscar_reserva,
    registrar_checkin,
    registrar_early_checkin,
    buscar_habitaciones_disponibles,
    registrar_walkin,
    agregar_cargo_checkout,
    extender_estadia,
    registrar_checkout,
    registrar_late_checkout,
    obtener_total_deuda,
    registrar_early_checkout as registrar_early_checkout_penalty,
    obtener_tipos_habitaciones,
    obtener_walkins,
    conectar_bd as conectar_db
)  

# --- CONFIGURACIÓN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(script_dir, "base_datos")
CHECKIN_HOUR = 14
EARLY_CHECKIN_PERCENT = 0.5

# ==========================
# FrontDeskApp 
# ==========================
class FrontDeskApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=CLARO)
        self.master = master
        self.pack(fill="both", expand=True)
        # selección actual
        self.selected_reserva = None
        self.selected_habitacion = None
        self.selected_checkout = None

        self.crear_dashboard()
        self.tab_control = ctk.CTkTabview(self, fg_color=CLARO)
        self.tab_checkin = self.tab_control.add("Check-in")
        self.tab_walkin = self.tab_control.add("Walk-in")
        self.tab_checkout = self.tab_control.add("Check-out")
        self.tab_control.pack(fill="both", expand=True, pady=10)

        self.crear_checkin()
        self.crear_walkin()
        self.crear_checkout()
        self.actualizar_dashboard()

    # ---------------- Dashboard ----------------
    def crear_dashboard(self):
        self.dashboard_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.dashboard_frame.pack(pady=8, fill="x")
        self.dashboard_frame.rowconfigure(index=0, weight=0, minsize=109)
        self.dashboard_frame.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')
        crear_tarjetas_kpi(master=self.dashboard_frame, dict=KPI_FRONTDESK())

    def actualizar_dashboard(self):
        # The dashboard is now created dynamically with current data, so this method is no longer needed.
        # Re-creating the dashboard would be the way to "update" it if data changes.
        pass

    # ---------------- Check-in ----------------
    def crear_checkin(self):
        frame = ctk.CTkFrame(self.tab_checkin, fg_color=CLARO)
        frame.pack(pady=8, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Buscar Reserva (ID, Nombre o Habitación):", text_color=OSCURO).pack(anchor="w", padx=10, pady=6)
        self.ci_query = ctk.CTkEntry(frame, placeholder_text="Ingrese ID, nombre o habitación")
        self.ci_query.pack(fill="x", padx=10, pady=4)
        ctk.CTkButton(frame, text="Buscar", command=self.buscar_reserva_gui, fg_color=AZUL, text_color=BLANCO).pack(pady=6)

        # resultados como scrollable frame con filas seleccionables
        self.ci_resultados = ctk.CTkScrollableFrame(frame, fg_color=GRIS_CLARO3, corner_radius=6, height=150)
        self.ci_resultados.pack(fill="both", expand=True, padx=10, pady=6)
        self.ci_rows = []

        botones_frame = ctk.CTkFrame(frame, fg_color=CLARO)
        botones_frame.pack(pady=8)
        ctk.CTkButton(botones_frame, text="Confirmar Check-in", command=self.confirmar_checkin_gui, fg_color=VERDE1, text_color=BLANCO).pack(side="left", padx=6)
        ctk.CTkButton(botones_frame, text="Early Check-in", command=self.early_checkin_gui, fg_color=MAMEY, text_color=BLANCO).pack(side="left", padx=6)

    def _update_results_grid(self, scroll_frame, data_list_of_dicts, headers_map, select_attr):
        for w in scroll_frame.winfo_children():
            w.destroy()

        # Store data for selection
        scroll_frame.data_list = data_list_of_dicts
        scroll_frame.celdas = []

        headers = list(headers_map.values())
        
        # Create headers
        for c, header in enumerate(headers):
            lbl = ctk.CTkLabel(scroll_frame, text=header, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'), text_color=OSCURO)
            lbl.grid(row=0, column=c, sticky='nsew', padx=1, pady=1)
            scroll_frame.grid_columnconfigure(c, weight=1)
            borde = ctk.CTkFrame(master=scroll_frame, fg_color=GRIS, height=2)
            borde.grid(row=1, column=c, sticky='ew')

        # Create data rows
        for f, row_data_dict in enumerate(data_list_of_dicts, start=1):
            fila_widgets = []
            bg = 'transparent' if f % 2 != 0 else GRIS_CLARO4
            
            for c, key in enumerate(headers_map.keys()):
                cell_text = row_data_dict.get(key, '')
                if key == 'monto_pago' or key == 'precio_base':
                    cell_text = f"${(cell_text or 0):,.2f}"

                lbl = ctk.CTkLabel(scroll_frame, text=cell_text, fg_color=bg, text_color=OSCURO, font=(FUENTE, 12))
                lbl.grid(row=f*2, column=c, sticky='nsew', padx=1, pady=1)
                lbl.bind("<Button-1>", lambda e, r_idx=f-1, sf=scroll_frame, sa=select_attr: self._on_grid_row_select(sf, r_idx, sa))
                fila_widgets.append(lbl)
            scroll_frame.celdas.append(fila_widgets)

    def _on_grid_row_select(self, scroll_frame, row_index, select_attr):
        attr_map = {
            'reserva': ('selected_reserva', 'selected_reserva_row_index'),
            'checkout': ('selected_checkout', 'selected_checkout_row_index'),
            'habitacion': ('selected_habitacion', 'selected_habitacion_row_index')
        }
        if select_attr not in attr_map:
            return

        data_attr, index_attr = attr_map[select_attr]
        
        current_index = getattr(self, index_attr, None)

        # Deselect if clicking the same row
        if current_index == row_index:
            setattr(self, data_attr, None)
            setattr(self, index_attr, None)
            new_index = None
        else:
            # Select the new row
            selected_data = scroll_frame.data_list[row_index]
            setattr(self, data_attr, selected_data)
            setattr(self, index_attr, row_index)
            new_index = row_index

        # Update highlighting
        for f, fila_widgets in enumerate(scroll_frame.celdas):
            is_selected = (f == new_index)
            new_bg = AZUL_CLARO if is_selected else ('transparent' if (f+1) % 2 != 0 else GRIS_CLARO4)
            for w in fila_widgets:
                w.configure(fg_color=new_bg)
        
        # Special logic for walk-in total calculation
        if select_attr == 'habitacion':
            self._update_walkin_total()

    def buscar_reserva_gui(self):
        query = self.ci_query.get().strip()
        try:
            resultados = buscar_reserva(query)
        except Exception as e:
            messagebox.showerror("Error DB", f"No se pudo buscar reservas: {e}")
            return
        
        headers = {
            'id': 'ID', 'cliente_nombre': 'Cliente', 'numero_hab': 'Hab.',
            'fecha_entrada': 'Entrada', 'fecha_salida': 'Salida',
            'monto_pago': 'Monto', 'estado': 'Estado'
        }
        self._update_results_grid(self.ci_resultados, resultados, headers, 'reserva')

    def confirmar_checkin_gui(self):
        if not self.selected_reserva:
            messagebox.showwarning("Aviso", "Seleccione una reserva (haga click en una fila).")
            return
        estado = self.selected_reserva['estado']
        if estado != "Pendiente":
            messagebox.showwarning("Aviso", f"La reserva ya está en estado: {estado}")
            return
        reserva_id = self.selected_reserva['id']
        try:
            registrar_checkin(reserva_id)
            messagebox.showinfo("Éxito", "Check-in registrado con éxito.")
            self.buscar_reserva_gui()
            self.actualizar_dashboard()
            self.selected_reserva = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el Check-in. Error: {e}")

    def early_checkin_gui(self):
        if not self.selected_reserva:
            messagebox.showwarning("Aviso","Seleccione una reserva.")
            return
        row = self.selected_reserva
        reserva_id = row['id']
        estado = row['estado']
        if estado != "Pendiente":
            messagebox.showwarning("Aviso","La reserva no está en estado 'Pendiente'.")
            return
        numero = row['numero_hab']
        conn = conectar_db()
        if not conn:
            messagebox.showerror("Error DB", "No se pudo conectar a la base de datos.")
            return
        cur = conn.cursor()
        cur.execute("SELECT estado FROM habitaciones WHERE numero=?", (numero,))
        hab = cur.fetchone()
        conn.close()
        if not hab or hab['estado'] != 'Disponible':
            messagebox.showerror("No disponible", "La habitación NO está libre ahora; no se puede hacer early check-in.")
            return
        conn = conectar_db()
        if not conn:
            messagebox.showerror("Error DB", "No se pudo conectar a la base de datos.")
            return
        cur = conn.cursor()
        cur.execute("SELECT monto_pago FROM reservas WHERE id=?", (reserva_id,))
        datos = cur.fetchone()
        precio_noche = 0.0
        if datos and datos['monto_pago'] is not None and float(datos['monto_pago'])>0:
            precio_noche = float(datos['monto_pago'])
        else:
            cur.execute("""
                SELECT t.precio_base FROM habitaciones h
                JOIN tipos_habitacion t ON h.tipo_id = t.id
                WHERE h.numero = ?
            """, (numero,))
            r = cur.fetchone()
            if r:
                precio_noche = float(r['precio_base'])
        conn.close()
        if precio_noche <= 0:
            messagebox.showerror("Error", "No se pudo determinar el precio por noche para esta habitación.")
            return
        monto_sugerido = round(precio_noche * EARLY_CHECKIN_PERCENT, 2)
        if not messagebox.askyesno("Early Check-in", f"Reserva ID: {reserva_id}\nHabitación: {numero}\nCargo sugerido: ${monto_sugerido:,.2f}\n¿Confirmar?"):
            return
        try:
            registrar_early_checkin(reserva_id, monto_sugerido)
            messagebox.showinfo("Éxito", "Early Check-in registrado y cobrado.")
            self.buscar_reserva_gui()
            self.actualizar_dashboard()
            self.selected_reserva = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el early check-in. Error: {e}")

    # ---------------- Walk-in ----------------
    def crear_walkin(self):
        for widget in self.tab_walkin.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.tab_walkin, fg_color=CLARO)
        frame.pack(pady=8, fill="both", expand=True)
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)

        # --- Sección de Datos del Cliente ---
        cliente_frame = ctk.CTkFrame(frame, fg_color='transparent')
        cliente_frame.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=(0, 10))
        cliente_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(cliente_frame, text="Datos del Cliente", font=(FUENTE, 14, 'bold'), text_color=OSCURO).grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 5))
        
        ctk.CTkLabel(cliente_frame, text="Nombre:", text_color=OSCURO).grid(row=1, column=0, padx=(0,5), pady=6, sticky="w")
        self.w_name = ctk.CTkEntry(cliente_frame); self.w_name.grid(row=1, column=1, padx=5, pady=6, sticky="ew")
        
        ctk.CTkLabel(cliente_frame, text="Email:", text_color=OSCURO).grid(row=1, column=2, padx=5, pady=6, sticky="w")
        self.w_email = ctk.CTkEntry(cliente_frame); self.w_email.grid(row=1, column=3, padx=(5,0), pady=6, sticky="ew")

    # --- Sección de Búsqueda de Habitación ---
        busqueda_frame = ctk.CTkFrame(frame, fg_color='transparent')
        busqueda_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        busqueda_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(busqueda_frame, text="Buscar Disponibilidad", font=(FUENTE, 14, 'bold'), text_color=OSCURO).grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 5))

        ctk.CTkLabel(busqueda_frame, text="Fecha Entrada (YYYY-MM-DD):", text_color=OSCURO).grid(row=1, column=0, padx=(0,5), pady=6, sticky="w")
        self.w_fecha_entrada = ctk.CTkEntry(busqueda_frame); self.w_fecha_entrada.grid(row=1, column=1, padx=5, pady=6, sticky="ew")
        self.w_fecha_entrada.insert(0, date.today().isoformat())
        
        ctk.CTkLabel(busqueda_frame, text="Fecha Salida (YYYY-MM-DD):", text_color=OSCURO).grid(row=1, column=2, padx=5, pady=6, sticky="w")
        self.w_fecha_salida = ctk.CTkEntry(busqueda_frame); self.w_fecha_salida.grid(row=1, column=3, padx=(5,0), pady=6, sticky="ew")
        
        ctk.CTkLabel(busqueda_frame, text="Tipo Habitación:", text_color=OSCURO).grid(row=2, column=0, padx=(0,5), pady=6, sticky="w")
        tipos_data = obtener_tipos_habitaciones()
        tipos = [row['nombre'] for row in tipos_data] if tipos_data else []
        self.w_tipo = ctk.CTkComboBox(busqueda_frame, values=tipos); self.w_tipo.grid(row=2, column=1, padx=5, pady=6, sticky="ew")
        
        ctk.CTkLabel(busqueda_frame, text="No. Personas:", text_color=OSCURO).grid(row=2, column=2, padx=5, pady=6, sticky="w")
        self.w_personas = ctk.CTkEntry(busqueda_frame); self.w_personas.grid(row=2, column=3, padx=(5,0), pady=6, sticky="ew")
    
        ctk.CTkButton(busqueda_frame, text="Buscar Habitaciones Disponibles", command=self.buscar_habitaciones_gui, fg_color=AZUL, text_color=BLANCO).grid(row=3, column=0, columnspan=4, pady=10)

    # --- Resultados y Confirmación ---
        self.w_habitaciones_frame = ctk.CTkScrollableFrame(frame, fg_color=GRIS_CLARO3, corner_radius=6, height=80)
        self.w_habitaciones_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.selected_habitacion = None

        self.w_monto_label = ctk.CTkLabel(frame, text="Monto Total Estimado: $0.00", text_color=OSCURO, font=(FUENTE, 13, 'bold'))
        self.w_monto_label.grid(row=3, column=0, columnspan=4, pady=6)

    # --- Botones de Confirmar y Ver Historial ---
        ctk.CTkButton(frame, text="Confirmar Walk-in", command=self.confirmar_walkin_gui, fg_color=VERDE1, text_color=BLANCO).grid(row=4, column=2, pady=10, padx=6, sticky='ew')
        ctk.CTkButton(frame, text="Ver historial de Walk-ins", command=self.historial_walkin, fg_color=AZUL, text_color=BLANCO).grid(row=4, column=3, pady=10, padx=6, sticky='ew')


    def historial_walkin(self):
    # Limpia el frame principal de la pestaña walk-in
        for widget in self.tab_walkin.winfo_children():
            widget.destroy()

    # Encabezado y estilo de botón activo
        ctk.CTkLabel(self.tab_walkin, 
                 text='📚 Historial de Walk-ins',
                 text_color=PRIMARIO,
                 font=(FUENTE, TAMANO_1, 'bold')
                 ).pack(pady=6, padx=12, anchor='w')

    # Frame para la tabla
        contenedor_tabla = ctk.CTkFrame(self.tab_walkin, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        contenedor_tabla.pack(fill='both', expand=True, padx=12, pady=12)

    # Encabezados
        encabezados = ["ID", "Hab.", "Cliente", "Email", "Entrada", "Salida", "Personas", "Estado"]
        data_tabla = [encabezados]

    # Obtiene los walk-ins registrados
        walkins = obtener_walkins()
        for w in walkins:
                fila = [w["id"], w["numero_hab"], w["cliente_nombre"], w["cliente_email"], w["fecha_entrada"], w["fecha_salida"], w["total_personas"], w["estado"]]
                data_tabla.append(fila)
        self.tabla_walkin(data=data_tabla, contenedor=contenedor_tabla)
        
        ctk.CTkButton(self.tab_walkin, text="Volver atrás", command=self.crear_walkin, fg_color=ROJO, text_color=BLANCO).pack(pady=10)

    # Muestra la tabla
    def tabla_walkin(self, data, contenedor):
    # Limpia el contenedor
        for w in contenedor.winfo_children():
            w.destroy()

        frame = ctk.CTkScrollableFrame(master=contenedor, fg_color='transparent')
        frame.pack(fill='both', expand=True, padx=12, pady=12)

    # Colores para estados
        colores = {
            'Completada': VERDE1, 
            'En curso': AZUL, 
            'Pendiente': MAMEY, 
            'Cancelada': ROJO,
        }

        self.celdas_walkin = []
        for f, fila in enumerate(data):
            fila_widgets = []
            for c, texto in enumerate(fila):
            # Coloreado de las líneas
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

            # Resaltado de estado con "pilas"
                if texto in colores:
                    cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                    cont_pila.grid(row=f*2, column=c, sticky='nsew', padx=1, pady=1)

                    pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height=28)
                    pila.pack(fill='y')

                    lbl = ctk.CTkLabel(master=pila, text=texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                    lbl.pack(expand=True, padx=8, pady=2)

                    widget_celda = (lbl, True)
                else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width=140, height=28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row=f*2, column=c, sticky='nsew', padx=1, pady=1)
                    widget_celda = (lbl, False)
            
                frame.grid_columnconfigure(c, weight=1)

            # Borde encabezado
                if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column=c, sticky='ew')
                    borde.grid_propagate(False)
                    borde.configure(height=2)

                fila_widgets.append(widget_celda)
            self.celdas_walkin.append(fila_widgets)

    def buscar_habitaciones_gui(self):
        f_entrada_str = self.w_fecha_entrada.get()
        f_salida_str = self.w_fecha_salida.get()
        tipo = self.w_tipo.get()
        f_entrada = validar_fecha(f_entrada_str)
        f_salida = validar_fecha(f_salida_str)
        if not f_entrada or not f_salida:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
            return
        if f_entrada >= f_salida:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada.")
            return
        if not tipo:
            messagebox.showwarning("Aviso", "Seleccione un tipo de habitación")
            return
        
        try:
            habitaciones = buscar_habitaciones_disponibles(f_entrada_str, f_salida_str, tipo)
        except Exception as e:
            messagebox.showerror("Error DB", f"No se pudo buscar habitaciones: {e}")
            return
        
        if not habitaciones:
            messagebox.showinfo("Aviso", "No se encontraron habitaciones disponibles.")

        headers = {'numero': 'Número', 'tipo_nombre': 'Tipo', 'precio_base': 'Precio Base'}
        self._update_results_grid(self.w_habitaciones_frame, habitaciones, headers, 'habitacion')
        
        self.selected_habitacion = None
        self.w_monto_label.configure(text="Monto Total Estimado: $0.00")

    def _update_walkin_total(self):
        if not self.selected_habitacion:
            self.w_monto_label.configure(text="Monto Total Estimado: $0.00")
            return
        
        f_entrada = validar_fecha(self.w_fecha_entrada.get())
        f_salida = validar_fecha(self.w_fecha_salida.get())
        if not f_entrada or not f_salida or f_entrada >= f_salida:
            self.w_monto_label.configure(text="Monto Total Estimado: 0 (Revise las fechas)")
            return
        
        dias = (f_salida - f_entrada).days
        monto_total = float(self.selected_habitacion['precio_base']) * dias
        self.w_monto_label.configure(text=f"Monto Total Estimado ({dias} noches): ${monto_total:,.2f}")

    def confirmar_walkin_gui(self):
        if not self.selected_habitacion:
            messagebox.showwarning("Aviso", "Seleccione una habitación de la lista.")
            return
        nombre = self.w_name.get().strip()
        f_entrada_str = self.w_fecha_entrada.get().strip()
        f_salida_str = self.w_fecha_salida.get().strip()
        personas_str = self.w_personas.get().strip()
        if not all([nombre, f_entrada_str, f_salida_str, personas_str]):
            messagebox.showwarning("Aviso", "Complete todos los datos.")
            return
        f_entrada = validar_fecha(f_entrada_str)
        f_salida = validar_fecha(f_salida_str)
        if not f_entrada or not f_salida or f_entrada >= f_salida:
            messagebox.showerror("Error de Fecha", "Fechas inválidas.")
            return
        try:
            personas = int(personas_str)
        except ValueError:
            messagebox.showerror("Error","Número de personas inválido.")
            return
        dias = (f_salida - f_entrada).days
        precio_base = float(self.selected_habitacion['precio_base'])
        monto_pago = precio_base * dias
        numero_hab = self.selected_habitacion['numero']
        if not messagebox.askyesno("Confirmar Cobro", f"Cliente: {nombre}\nHabitación: {numero_hab}\nTotal: ${monto_pago:,.2f}\n¿Confirmar?"):
            return
        try:
            registrar_walkin(nombre, self.w_email.get().strip(), f_entrada_str, f_salida_str, personas, monto_pago, numero_hab)
            messagebox.showinfo("Éxito", "Walk-in registrado.")
            self.actualizar_dashboard()
            self.w_name.delete(0, "end")
            self.w_email.delete(0, "end")
            self.w_personas.delete(0, "end")
            # Limpiar la tabla de resultados
            headers = {'numero': 'Número', 'tipo_nombre': 'Tipo', 'precio_base': 'Precio Base'}
            self._update_results_grid(self.w_habitaciones_frame, [], headers, 'habitacion')
            self.w_monto_label.configure(text="Monto Total Estimado: $0.00")
            self.w_tipo.set("")
            self.selected_habitacion = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el Walk-in. Error: {e}")

    # ---------------- Check-out ----------------
    def crear_checkout(self):
        frame = ctk.CTkFrame(self.tab_checkout, fg_color=CLARO)
        frame.pack(pady=8, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1) # Allow self.co_resultados to expand vertically
        frame.grid_rowconfigure(2, weight=0) # Ensure the "Cargar Check-outs de Hoy" button doesn't take extra space
        frame.grid_rowconfigure(3, weight=2) # Give more weight to opciones_frame for vertical expansion
        frame.grid_rowconfigure(4, weight=1, minsize=60) # Ensure the final button's row has a minimum height

        # --- Lista de Check-outs ---
        ctk.CTkLabel(frame, text="Reservas para Check-out Hoy", font=(FUENTE, 14, 'bold'), text_color=OSCURO).grid(row=0, column=0, sticky='w', padx=10, pady=(0,5))
        self.co_resultados = ctk.CTkScrollableFrame(frame, fg_color=GRIS_CLARO3, corner_radius=6, height=100)
        self.co_resultados.grid(row=1, column=0, sticky='nsew', padx=10)
        ctk.CTkButton(frame, text="Cargar Check-outs de Hoy", command=self.cargar_checkouts, fg_color=AZUL, text_color=BLANCO).grid(row=2, column=0, pady=10)

        # --- Opciones de Check-out ---
        opciones_frame = ctk.CTkFrame(frame, fg_color='transparent')
        opciones_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        opciones_frame.grid_columnconfigure((0, 1), weight=1)
        opciones_frame.grid_rowconfigure(0, weight=1) # Allow the first row (cargo and extend frames) to expand
        opciones_frame.grid_rowconfigure(1, weight=1) # Allow the second row (early checkout frame) to expand

        # --- Agregar Cargos ---
        cargo_frame = ctk.CTkFrame(opciones_frame, fg_color='transparent')
        cargo_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        ctk.CTkLabel(cargo_frame, text="Agregar Cargo Adicional", font=(FUENTE, 13, 'bold'), text_color=OSCURO).pack(fill="x", pady=(0,5))
        
        # New frame for buttons
        cargo_buttons_frame = ctk.CTkFrame(cargo_frame, fg_color='transparent')
        cargo_buttons_frame.pack(fill="x", pady=5)
        cargo_buttons_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(cargo_buttons_frame, text="Cargos", command=self.abrir_modal_cargos_adicionales, fg_color=MAMEY, text_color=BLANCO).grid(row=0, column=0, padx=(0, 5), sticky='ew')
        ctk.CTkButton(cargo_buttons_frame, text="Cobro", command=self.cobro_gui, fg_color=AZUL, text_color=BLANCO).grid(row=0, column=1, padx=(5, 0), sticky='ew')

        # --- Check-out Anticipado ---
        early_checkout_frame = ctk.CTkFrame(opciones_frame, fg_color='transparent')
        early_checkout_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 5), pady=(10,10))
        ctk.CTkLabel(early_checkout_frame, text="Check-out Anticipado", font=(FUENTE, 13, 'bold'), text_color=OSCURO).pack(fill="x", pady=(0,5))
        ctk.CTkButton(early_checkout_frame, text="Confirmar C/O Anticipado (Modificado)", command=self.early_checkout_gui, fg_color=ROJO, text_color=BLANCO).pack(fill="x", pady=(5,0))

        # --- Extender Estadía y Late Check-out ---
        ext_late_frame = ctk.CTkFrame(opciones_frame, fg_color='transparent')
        ext_late_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=(5, 0)) # Add rowspan
        ext_late_frame.grid_columnconfigure(1, weight=1)
        ext_late_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1) # Allow all internal rows to expand
        
        ctk.CTkLabel(ext_late_frame, text="Extender Estadía", font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,5))
        ctk.CTkLabel(ext_late_frame, text="Nueva fecha (YYYY-MM-DD):", text_color=OSCURO).grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self.co_nueva_salida = ctk.CTkEntry(ext_late_frame); self.co_nueva_salida.grid(row=1, column=1, padx=5, pady=4, sticky="ew")
        ctk.CTkButton(ext_late_frame, text="Extender", command=self.extender_estadia_gui, fg_color=AZUL, text_color=BLANCO).grid(row=2, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(ext_late_frame, text="Late Check-Out", font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=3, column=0, columnspan=2, sticky='w', pady=(10,5))
        ctk.CTkLabel(ext_late_frame, text="Cargo:", text_color=OSCURO).grid(row=4, column=0, padx=5, pady=4, sticky="w")
        self.late_cargo = ctk.CTkEntry(ext_late_frame); self.late_cargo.grid(row=4, column=1, padx=5, pady=4, sticky="ew")
        self.late_cargo.insert(0, "50.00")
        ctk.CTkButton(ext_late_frame, text="Aplicar Late C/O", command=self.late_checkout_gui, fg_color=MAMEY, text_color=BLANCO).grid(row=5, column=0, columnspan=2, pady=10)

        # --- Confirmación Final ---
        ctk.CTkButton(frame, text="Confirmar Check-out Final", command=self.confirmar_checkout_gui, fg_color=VERDE1, text_color=BLANCO, height=35).grid(row=4, column=0, pady=10, padx=10, sticky='s')

    def cargar_checkouts(self):
        conn = conectar_db()
        if not conn:
            messagebox.showerror("Error DB", "No se pudo conectar a la base de datos.")
            return
        hoy = date.today().isoformat()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT r.id, c.nombres || ' ' || c.apellidos as cliente_nombre, r.numero_hab,
                       r.fecha_entrada, r.fecha_salida, r.monto_pago, r.estado
                FROM reservas r
                JOIN clientes c ON r.id_cliente = c.id
                WHERE r.estado='checked-in' AND r.fecha_salida <= ?
            """, (hoy,))
            resultados = [dict(row) for row in cur.fetchall()]
            if not resultados:
                messagebox.showinfo("Sin resultados", "No hay reservas en estado 'checked-in' con fecha de salida hoy o anterior.")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar check-outs: {e}")
            resultados = []
        finally:
            conn.close()

        headers = {
            'id': 'ID', 'cliente_nombre': 'Cliente', 'numero_hab': 'Hab.',
            'fecha_entrada': 'Entrada', 'fecha_salida': 'Salida',
            'monto_pago': 'Monto', 'estado': 'Estado'
        }
        self._update_results_grid(self.co_resultados, resultados, headers, 'checkout')

    def abrir_modal_cargos_adicionales(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso", "Seleccione una reserva en Check-out para agregar cargos.")
            return
        
        reserva_id = self.selected_checkout['id']
        # Pass the instance's method as a callback to the modal
        ModalCargosAdicionales(self.master, reserva_id, self._callback_cargo_agregado)

    def _callback_cargo_agregado(self, reserva_id, concepto, descripcion, monto):
        try:
            agregar_cargo_checkout(reserva_id, concepto, descripcion, monto)
            messagebox.showinfo("Éxito", "Cargo agregado al total de la reserva.")
            self.cargar_checkouts()
            self.actualizar_dashboard()
            self.selected_checkout = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo agregar el cargo. Error: {e}")

    def extender_estadia_gui(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso","Seleccione una reserva.")
            return
        reserva_id = self.selected_checkout['id']
        nueva_salida_str = self.co_nueva_salida.get().strip()
        fecha_actual_salida_str = self.selected_checkout['fecha_salida']
        nueva_salida = validar_fecha(nueva_salida_str)
        fecha_actual_salida = validar_fecha(fecha_actual_salida_str)
        if not nueva_salida:
            messagebox.showerror("Error de Fecha", "Formato de fecha de salida inválido (YYYY-MM-DD).")
            return
        if not fecha_actual_salida:
            messagebox.showerror("Error de Datos", "No se pudo leer la fecha de salida actual.")
            return
        if nueva_salida <= fecha_actual_salida:
            messagebox.showerror("Error de Extensión", "La nueva fecha de salida debe ser posterior a la actual.")
            return
        try:
            extender_estadia(reserva_id, nueva_salida_str)
            messagebox.showinfo("Éxito","Estadía extendida con éxito.")
            self.cargar_checkouts()
            self.selected_checkout = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo extender la estadía. Error: {e}")

    def confirmar_checkout_gui(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso","Seleccione una reserva.")
            return
        reserva_id = self.selected_checkout['id']
        if not messagebox.askyesno("Confirmar Check-out", f"¿Confirma la salida de la reserva ID {reserva_id}?"):
            return
        try:
            registrar_checkout(reserva_id)
            messagebox.showinfo("Éxito","Check-out confirmado. Habitación liberada.")
            self.cargar_checkouts()
            self.actualizar_dashboard()
            self.selected_checkout = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo completar el Check-out. Error: {e}")

    def cobro_gui(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso", "Seleccione una reserva en Check-out para realizar un cobro.")
            return
        
        reserva_id = self.selected_checkout['id']
        total_deuda = obtener_total_deuda(reserva_id)
        
        ModalCobro(self.master, reserva_id, total_deuda)

    def late_checkout_gui(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso", "Seleccione una reserva.")
            return

        # Validar el estado de la reserva
        estado_reserva = self.selected_checkout['estado']
        if estado_reserva != "checked-in":
            messagebox.showwarning("Aviso", f"No se puede realizar Late Check-Out para reservas en estado: {estado_reserva}.")
            return

        numero_hab = self.selected_checkout['numero_hab']
        conn = conectar_db()
        if not conn:
            messagebox.showerror("Error DB", "No se pudo conectar a la base de datos.")
            return

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM reservas WHERE numero_hab=? AND fecha_entrada > ?", (numero_hab, date.today().isoformat()))
        r = cur.fetchone()
        conn.close()

        if r and r['cnt'] > 0:
            messagebox.showerror("No disponible", "La habitación está reservada después; no se puede realizar Late Check-Out.")
            return

        try:
            monto_cargo = float(self.late_cargo.get())
            if monto_cargo <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "El cargo por Late Check-Out debe ser un número positivo.")
            return

        if not messagebox.askyesno("Late Check-Out", f"Reserva ID: {self.selected_checkout['id']}\nHabitación: {numero_hab}\nCargo: ${monto_cargo:,.2f}\n¿Confirmar?"):
            return

        try:
            registrar_late_checkout(self.selected_checkout['id'], monto_cargo)
            messagebox.showinfo("Éxito", "Late Check-Out registrado y cobrado.")
            self.cargar_checkouts()
            self.actualizar_dashboard()
            self.selected_checkout = None
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el Late Check-Out. Error: {e}")

    def early_checkout_gui(self):
        if not self.selected_checkout:
            messagebox.showwarning("Aviso", "Seleccione una reserva.")
            return
        
        reserva_id = self.selected_checkout['id']
        fecha_salida_programada = validar_fecha(self.selected_checkout['fecha_salida'])
        hoy = date.today()

        if not fecha_salida_programada:
            messagebox.showerror("Error de Fecha", "No se pudo obtener la fecha de salida programada.")
            return

        if hoy >= fecha_salida_programada:
            messagebox.showwarning("Aviso", "La fecha de salida programada ya ha pasado o es hoy. Use el Check-out normal.")
            return
        
        # Open the modal for early checkout confirmation
        ModalEarlyCheckout(self.master, reserva_id, fecha_salida_programada, self._callback_early_checkout)

    def _callback_early_checkout(self, reserva_id, motivo_salida):
        conn = None # Initialize conn to None
        try:
            conn = conectar_db()
            if not conn:
                raise Exception("No se pudo conectar a la base de datos.")
            cur = conn.cursor()
            
            # Get reservation details
            cur.execute("SELECT fecha_entrada, fecha_salida, monto_pago, numero_hab FROM reservas WHERE id=?", (reserva_id,))
            reserva_data = cur.fetchone()
            
            if not reserva_data:
                raise Exception("Reserva no encontrada para check-out anticipado.")

            fecha_entrada = validar_fecha(reserva_data['fecha_entrada'])
            fecha_salida_programada = validar_fecha(reserva_data['fecha_salida'])
            monto_total_reserva = float(reserva_data['monto_pago'])
            numero_hab = reserva_data['numero_hab']

            if not fecha_entrada or not fecha_salida_programada:
                raise Exception("Fechas de reserva inválidas.")

            dias_totales = (fecha_salida_programada - fecha_entrada).days
            dias_restantes = (fecha_salida_programada - date.today()).days

            if dias_totales <= 0:
                precio_noche = 0 # Avoid division by zero if reservation is for 0 or negative days
            else:
                precio_noche = monto_total_reserva / dias_totales

            penalizacion = 0.0
            if dias_restantes > 0:
                penalizacion = round(precio_noche * dias_restantes * EARLY_CHECKOUT_PENALTY_PERCENT, 2)

            # Update reservation status and room status
            cur.execute("UPDATE reservas SET estado='Completada', checked_out=1, notas=? WHERE id=?", (motivo_salida, reserva_id))
            cur.execute("UPDATE habitaciones SET estado='Sucia' WHERE numero=?", (numero_hab,))
            cur.execute("INSERT INTO checkins_checkouts (reserva_id, tipo, notas) VALUES (?, 'checkout_anticipado', ?)", (reserva_id, motivo_salida))
            
            # Add penalty as an additional charge if applicable
            if penalizacion > 0:
                cur.execute("""
                    INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago, notas)
                    VALUES (?, ?, ?, ?, ?)
                """, ('costo_adicional_checkout', 'Penalización por Check-out Anticipado', penalizacion, 'efectivo', f'Reserva ID: {reserva_id} - {motivo_salida}'))
            
            conn.commit()
            messagebox.showinfo("Éxito", f"Check-out anticipado registrado con éxito. Habitación {numero_hab} en limpieza. Penalización aplicada: ${penalizacion:,.2f}")
            self.cargar_checkouts()
            self.actualizar_dashboard()
            self.selected_checkout = None

        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo completar el Check-out anticipado. Error: {e}")
        finally:
            if conn:
                conn.close()

# ==========================
# ModalCargosAdicionales
# ==========================
class ModalCargosAdicionales(ctk.CTkToplevel):
    def __init__(self, master, reserva_id, callback_agregar_cargo):
        super().__init__(master = master, fg_color=CLARO)
        self.reserva_id = reserva_id
        self.callback_agregar_cargo = callback_agregar_cargo # Function to call when saving
        
        self.title("Agregar Cargo Adicional")
        self.geometry("450x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # Title
        ctk.CTkLabel(self, 
                     text="➕ Agregar Cargo Adicional", 
                     text_color=OSCURO, 
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor='w', pady=(16,0), padx=16)
        
        ctk.CTkFrame(self, height=2, fg_color=OSCURO).pack(fill='x', padx=15, pady=10)

        self.crear_formulario()

    def crear_formulario(self):
        frame_formulario = ctk.CTkFrame(master=self, fg_color='transparent')
        frame_formulario.pack(fill='both', expand=True, padx=15)
        frame_formulario.columnconfigure(1, weight=1)

        # Variables de los campos
        self.concepto_var = ctk.StringVar()
        self.descripcion_var = ctk.StringVar()
        self.monto_var = ctk.StringVar()

        # Concepto
        ctk.CTkLabel(master=frame_formulario,
                     text='Concepto:',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row=0, column=0, sticky='w', pady=6, padx=(0,10))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=self.concepto_var,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row=0, column=1, sticky='ew', pady=6)
        
        # Descripción
        ctk.CTkLabel(master=frame_formulario,
                     text='Descripción:',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row=1, column=0, sticky='w', pady=6, padx=(0,10))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=self.descripcion_var,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row=1, column=1, sticky='ew', pady=6)

        # Monto
        ctk.CTkLabel(master=frame_formulario,
                     text='Monto:',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row=2, column=0, sticky='w', pady=6, padx=(0,10))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=self.monto_var,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row=2, column=1, sticky='ew', pady=6)
        
        # Botones
        button_frame = ctk.CTkFrame(master=frame_formulario, fg_color='transparent')
        button_frame.grid(row=3, column=0, columnspan=2, pady=12)

        Boton(master=button_frame,
              texto='Cancelar',
              color=PRIMARIO,
              hover=ROJO,
              metodo=self.destroy
              ).pack(side='left', padx=10)
        
        Boton(master=button_frame,
              texto='Guardar Cargo',
              color=VERDE1,
              hover=VERDE2,
              metodo=self.guardar_cargo
              ).pack(side='left', padx=10)

    def guardar_cargo(self):
        concepto = self.concepto_var.get().strip()
        descripcion = self.descripcion_var.get().strip()
        monto_str = self.monto_var.get().strip()

        if not concepto or not descripcion or not monto_str:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return
        
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Monto inválido. Debe ser un número positivo.")
            return
        
        # Call the callback function passed from FrontDeskApp
        if self.callback_agregar_cargo:
            self.callback_agregar_cargo(self.reserva_id, concepto, descripcion, monto)
            self.destroy() # Close the modal after saving

# ==========================
# ModalCobro
# ==========================
class ModalCobro(ctk.CTkToplevel):
    def __init__(self, master, reserva_id, monto_total_dop):
        super().__init__(master)
        self.master = master
        self.reserva_id = reserva_id
        self.monto_total_dop = monto_total_dop

        self.title("Registrar Pago")
        self.geometry("500x600")
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame Principal ---
        main_frame = ctk.CTkFrame(self, fg_color=CLARO)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)

        # --- Título ---
        ctk.CTkLabel(main_frame, text="Registrar pago", font=(FUENTE, 20, 'bold'), text_color=OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # --- Total en DOP ---
        ctk.CTkLabel(main_frame, text="Total en DOP", text_color=OSCURO).grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        self.total_dop_entry = ctk.CTkEntry(main_frame)
        self.total_dop_entry.grid(row=1, column=1, sticky="ew")
        self.total_dop_entry.insert(0, f"{self.monto_total_dop:.2f}")

        # --- Moneda ---
        ctk.CTkLabel(main_frame, text="Moneda", text_color=OSCURO).grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        self.moneda_optionmenu = ctk.CTkOptionMenu(main_frame, values=["DOP", "USD", "EUR"], command=self.actualizar_tasa)
        self.moneda_optionmenu.grid(row=2, column=1, sticky="ew")

        # --- Tasa ---
        ctk.CTkLabel(main_frame, text="Tasa", text_color=OSCURO).grid(row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        self.tasa_entry = ctk.CTkEntry(main_frame)
        self.tasa_entry.grid(row=3, column=1, sticky="ew")
        self.tasa_entry.bind("<KeyRelease>", self.actualizar_monto_equivalente)

        # Label para la fuente de la tasa
        self.tasa_fuente_label = ctk.CTkLabel(main_frame, text="Fuente: Manual", text_color=GRIS)
        self.tasa_fuente_label.grid(row=3, column=2, padx=10, sticky="w")
        # --- Monto Equivalente ---
        ctk.CTkLabel(main_frame, text="Monto equivalente", text_color=OSCURO).grid(row=4, column=0, padx=(0, 10), pady=10, sticky="w")
        self.monto_equivalente_entry = ctk.CTkEntry(main_frame, state="readonly")
        self.monto_equivalente_entry.grid(row=4, column=1, sticky="ew")

        # --- Botón Registrar Pago ---
        ctk.CTkButton(main_frame, text="Registrar pago", command=self.registrar_pago, fg_color=VERDE1, text_color=BLANCO).grid(row=5, column=0, columnspan=2, pady=20)

        # --- Historial de Pagos ---
        historial_frame = ctk.CTkFrame(self, fg_color=CLARO)
        historial_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        historial_frame.grid_columnconfigure(0, weight=1)
        historial_frame.grid_rowconfigure(1, weight=1)

        # ...existing code...
        self.tasa_entry = ctk.CTkEntry(main_frame)
        self.tasa_entry.grid(row=3, column=1, sticky="ew")
        self.tasa_entry.bind("<KeyRelease>", self.actualizar_monto_equivalente)

        # Label para la fuente de la tasa
        self.tasa_fuente_label = ctk.CTkLabel(main_frame, text="Fuente: Manual", text_color=GRIS)
        self.tasa_fuente_label.grid(row=3, column=2, padx=10, sticky="w")
        # ...existing code...
        ctk.CTkLabel(historial_frame, text="Historial de pagos", font=(FUENTE, 16, 'bold'), text_color=OSCURO).grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.historial_treeview = ttk.Treeview(historial_frame, columns=("ID", "ID reserva", "Monto local", "Moneda", "Tasa", "Monto equivalente", "Fecha"), show="headings")
        self.historial_treeview.heading("ID", text="ID")
        self.historial_treeview.heading("ID reserva", text="ID reserva")
        self.historial_treeview.heading("Monto local", text="Monto local")
        self.historial_treeview.heading("Moneda", text="Moneda")
        self.historial_treeview.heading("Tasa", text="Tasa")
        self.historial_treeview.heading("Monto equivalente", text="Monto equivalente")
        self.historial_treeview.heading("Fecha", text="Fecha")
        self.historial_treeview.grid(row=1, column=0, sticky="nsew")

        self.actualizar_tasa(self.moneda_optionmenu.get())
        self.cargar_historial_pagos()

    def actualizar_tasa(self, moneda):
        if moneda == "DOP":
            self.tasa_entry.delete(0, "end")
            self.tasa_entry.insert(0, "1.00")
            self.tasa_fuente_label.configure(text="Fuente: Manual")
            self.actualizar_monto_equivalente()
            return

        try:
            response = requests.get(f"https://api.exchangerate.host/latest?base=DOP&symbols={moneda}")
            response.raise_for_status()
            data = response.json()
            print("Respuesta de la API:", data)
            if "rates" in data and moneda in data["rates"]:
                tasa = data["rates"][moneda]
                self.tasa_entry.delete(0, "end")
                self.tasa_entry.insert(0, f"{tasa:.2f}")
                self.tasa_fuente_label.configure(text="Fuente: API exchangerate.host")
            else:
                raise KeyError("No se pudo obtener la tasa de cambio para la moneda seleccionada.")
        except Exception:
            tasa_default = {"USD": 58.0, "EUR": 63.0}
            self.tasa_entry.delete(0, "end")
            self.tasa_entry.insert(0, f"{tasa_default.get(moneda, 1.0):.2f}")
            self.tasa_fuente_label.configure(text="Fuente: Manual (predeterminada)")
            messagebox.showwarning("Advertencia", "No se pudo obtener la tasa de cambio en tiempo real. Usando tasa predeterminada.")
        self.actualizar_monto_equivalente()

    def actualizar_monto_equivalente(self, event=None):
        try:
            total_dop = float(self.total_dop_entry.get())
            tasa = float(self.tasa_entry.get())
            moneda = self.moneda_optionmenu.get()
            monto_equivalente = total_dop / tasa
            self.monto_equivalente_entry.configure(state="normal")
            self.monto_equivalente_entry.delete(0, "end")
            self.monto_equivalente_entry.insert(0, f"{monto_equivalente:.2f} {moneda}")
            self.monto_equivalente_entry.configure(state="readonly")
        except (ValueError, ZeroDivisionError):
            self.monto_equivalente_entry.configure(state="normal")
            self.monto_equivalente_entry.delete(0, "end")
            self.monto_equivalente_entry.insert(0, "Error")
            self.monto_equivalente_entry.configure(state="readonly")

    def registrar_pago(self):
        try:
            monto_local = float(self.total_dop_entry.get())
            moneda = self.moneda_optionmenu.get()
            tasa = float(self.tasa_entry.get())
            monto_equivalente = monto_local / tasa
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fuente_tasa = self.tasa_fuente_label.cget("text").replace("Fuente: ", "")

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pagos (id_reserva, monto_local, moneda, tasa, monto_equivalente, fecha, fuente_tasa)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.reserva_id, monto_local, moneda, tasa, monto_equivalente, fecha, fuente_tasa))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Pago registrado exitosamente.")
            self.cargar_historial_pagos()
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"No se pudo registrar el pago: {e}")

    def cargar_historial_pagos(self):
        for item in self.historial_treeview.get_children():
            self.historial_treeview.delete(item)

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, id_reserva, monto_local, moneda, tasa, monto_equivalente, fecha FROM pagos WHERE id_reserva = ? ORDER BY fecha DESC", (self.reserva_id,))
            pagos = cur.fetchall()
            conn.close()

            for pago in pagos:
                self.historial_treeview.insert("", "end", values=pago)
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar el historial de pagos: {e}")
class ModalEarlyCheckout(ctk.CTkToplevel):
    def __init__(self, master, reserva_id, fecha_salida_programada, callback):
        super().__init__(master)
        self.master = master
        self.reserva_id = reserva_id
        self.fecha_salida_programada = fecha_salida_programada
        self.callback = callback

        self.title("Confirmar Check-out Anticipado")
        self.geometry("400x250")
        self.transient(master) # Make modal
        self.grab_set() # Grab all events from the master
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(self, text="El huésped saldrá antes de la fecha prevista.", font=(FUENTE, 14, 'bold'), text_color=OSCURO).grid(row=0, column=0, padx=20, pady=(20,5), sticky="ew")
        ctk.CTkLabel(self, text=f"Fecha de salida programada: {self.fecha_salida_programada.isoformat()}", text_color=OSCURO).grid(row=1, column=0, padx=20, pady=(0,10), sticky="ew")
        ctk.CTkLabel(self, text="Motivo de salida anticipada (opcional):", text_color=OSCURO).grid(row=2, column=0, padx=20, pady=(0,5), sticky="w")
        
        self.motivo_entry = ctk.CTkEntry(self, placeholder_text="Ingrese el motivo")
        self.motivo_entry.grid(row=3, column=0, padx=20, pady=(0,10), sticky="ew")

        button_frame = ctk.CTkFrame(self, fg_color='transparent')
        button_frame.grid(row=4, column=0, pady=10)
        button_frame.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(button_frame, text="Confirmar", command=self._confirm, fg_color=VERDE1, text_color=BLANCO).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=self._on_closing, fg_color=ROJO, text_color=BLANCO).grid(row=0, column=1, padx=10)

    def _confirm(self):
        motivo = self.motivo_entry.get().strip()
        self.callback(self.reserva_id, motivo)
        self.destroy()

    def _on_closing(self):
        self.destroy()
