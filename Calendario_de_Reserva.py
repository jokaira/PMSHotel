import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from gestor_clientes import GestorClientes

###EN PROCESO DE INTEGRACION

class Habitacion:
    def __init__(self, numero, tipo, precio_por_noche):
        self.numero = numero
        self.tipo = tipo
        self.precio_por_noche = precio_por_noche

    def __str__(self):
        return f"Hab. {self.numero} ({self.tipo}) - ${self.precio_por_noche:.2f}/noche"

class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono=None):
        self.id = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"ID: {self.id} | {self.nombre} ({self.email})"

class Reserva:
    def __init__(self, id_reserva, numero_habitacion, id_cliente, fecha_entrada, fecha_salida):
        self.id = id_reserva
        self.numero_habitacion = numero_habitacion
        self.id_cliente = id_cliente
        self.fecha_entrada = fecha_entrada  # Almacenado como date object
        self.fecha_salida = fecha_salida    # Almacenado como date object

    def __str__(self):
        return (f"ID {self.id} | Hab: {self.numero_habitacion} | Cliente ID: {self.id_cliente} | "
                f"Ent: {self.fecha_entrada.strftime('%Y-%m-%d')} | Sal: {self.fecha_salida.strftime('%Y-%m-%d')}")

# --- Gestor de Base de Datos ---

class DatabaseManager:
    def __init__(self, db_name="base_datos.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()
        # self.create_tables() JSS: Comentado para que no me reescriba las tablas

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    # def create_tables(self): # JSS: comentado para que no me reescriba las tablas
    #     cursor = self.conn.cursor()
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS habitaciones (
    #             numero INTEGER PRIMARY KEY,
    #             tipo TEXT NOT NULL,
    #             precio_por_noche REAL NOT NULL
    #         )
    #     """)
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS clientes (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             nombre TEXT NOT NULL,
    #             email TEXT UNIQUE NOT NULL,
    #             telefono TEXT
    #         )
    #     """)
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS reservas (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             numero_habitacion INTEGER NOT NULL,
    #             id_cliente INTEGER NOT NULL,
    #             fecha_entrada TEXT NOT NULL,
    #             fecha_salida TEXT NOT NULL,
    #             FOREIGN KEY (numero_habitacion) REFERENCES habitaciones(numero),
    #             FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    #         )
    #     """)
    #     self.conn.commit()

    # --- Métodos para Habitaciones  ---
    # def insert_habitacion(self, habitacion): JSS: comentada, ya que está el módilo de habitaciones.
    #     cursor = self.conn.cursor()
    #     try:
    #         cursor.execute("INSERT INTO habitaciones (numero, tipo, precio_por_noche) VALUES (?, ?, ?)",
    #                        (habitacion.numero, habitacion.tipo, habitacion.precio_por_noche))
    #         self.conn.commit()
    #         return True, "Habitación agregada exitosamente."
    #     except sqlite3.IntegrityError:
    #         return False, f"La habitación {habitacion.numero} ya existe."
    #     except Exception as e:
    #         return False, f"Error al agregar habitación: {e}"

    def get_all_habitaciones(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT numero_habitacion as numero, TiposHabitacion.nombre_tipo as tipo, TiposHabitacion.precio_default as precio_por_noche 
                       FROM Habitaciones
                       INNER JOIN TiposHabitacion
                       ON Habitaciones.id_tipo_habitacion = TiposHabitacion.id_tipo_habitacion 
                       ORDER BY numero ASC""") #JSS: modificado para que coincida con las tablas del modulo de habitaciones
        return [Habitacion(row['numero'], row['tipo'], row['precio_por_noche']) for row in cursor.fetchall()]

    def get_habitacion_by_numero(self, numero):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT numero_habitacion as numero, TiposHabitacion.nombre_tipo as tipo, TiposHabitacion.precio_default as precio_por_noche 
                       FROM Habitaciones
                       INNER JOIN TiposHabitacion
                       ON Habitaciones.id_tipo_habitacion = TiposHabitacion.id_tipo_habitacion 
                       WHERE numero = ?""", (numero,)) #JSS: modificado para que coincida con las tablas del modulo de habitaciones
        row = cursor.fetchone()
        if row:
            return Habitacion(row['numero'], row['tipo'], row['precio_por_noche'])
        return None

    # --- Métodos para Clientes ---
    # def insert_cliente(self, cliente): JSS: Comentado porque todo esto lo hará el módulo de clientes
    #     cursor = self.conn.cursor()
    #     try:
    #         cursor.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)",
    #                        (cliente.nombre, cliente.email, cliente.telefono))
    #         self.conn.commit()
    #         return True, cursor.lastrowid, "Cliente agregado exitosamente."
    #     except sqlite3.IntegrityError:
    #         return False, None, f"El email {cliente.email} ya está registrado."
    #     except Exception as e:
    #         return False, None, f"Error al agregar cliente: {e}"
    
    def get_all_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_cliente as id, nombres || ' ' || apellidos as nombre, email, telefono FROM cliente ORDER BY nombre ASC")
        #modificado para que coincida con la tabla del modulo de clientes
        return [Cliente(row['id'], row['nombre'], row['email'], row['telefono']) for row in cursor.fetchall()]

    def get_cliente_by_id(self, id_cliente):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_cliente as id, nombres || ' ' || apellidos as nombre, email, telefono FROM cliente WHERE id = ?", (id_cliente,))
        #modificado para que coincida con la tabla del modulo de clientes
        row = cursor.fetchone()
        if row:
            return Cliente(row['id'], row['nombre'], row['email'], row['telefono'])
        return None

    def get_cliente_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_cliente as id, nombres || ' ' || apellidos as nombre, email, telefono FROM cliente WHERE email = ?", (email,))
        #modificado para que coincida con la tabla del modulo de clientes
        row = cursor.fetchone()
        if row:
            return Cliente(row['id'], row['nombre'], row['email'], row['telefono'])
        return None

    # --- Métodos de CRUD para Reservas  ---
    def insert_reserva(self, reserva):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO reservas (numero_habitacion, id_cliente, fecha_entrada, fecha_salida) VALUES (?, ?, ?, ?)",
                           (reserva.numero_habitacion, reserva.id_cliente,
                            reserva.fecha_entrada.strftime('%Y-%m-%d'),
                            reserva.fecha_salida.strftime('%Y-%m-%d')))
            self.conn.commit()
            return True, cursor.lastrowid, "Reserva realizada exitosamente."
        except Exception as e:
            return False, None, f"Error al hacer la reserva: {e}"

    def get_all_reservas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT r.*, t.nombre_tipo as tipo, t.precio_default as precio_por_noche, c.nombres || ' ' || c.apellidos AS cliente_nombre, c.email AS cliente_email "
                       "FROM reservas r "
                       "INNER JOIN Habitaciones h ON r.numero_habitacion = h.numero_habitacion "
                       "INNER JOIN TiposHabitacion t ON h.id_tipo_habitacion = t.id_tipo_habitacion "
                       "INNER JOIN cliente c ON r.id_cliente = c.id_cliente "
                       "ORDER BY r.fecha_entrada ASC")
        #modificado para que coincida con las tablas de los demás módulos

        reservas_completas = []
        for row in cursor.fetchall():
            reserva = {
                'id': row['id'],
                'numero_habitacion': row['numero_habitacion'],
                'tipo_habitacion': row['tipo'],
                'precio_por_noche': row['precio_por_noche'],
                'id_cliente': row['id_cliente'],
                'nombre_cliente': row['cliente_nombre'],
                'email_cliente': row['cliente_email'],
                'fecha_entrada': datetime.datetime.strptime(row['fecha_entrada'], '%Y-%m-%d').date(),
                'fecha_salida': datetime.datetime.strptime(row['fecha_salida'], '%Y-%m-%d').date()
            }
            reservas_completas.append(reserva)
        return reservas_completas

    def delete_reserva(self, id_reserva):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = ?", (id_reserva,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_reservas_for_habitacion_and_period(self, numero_habitacion, fecha_entrada, fecha_salida):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM reservas
            WHERE numero_habitacion = ?
            AND NOT (fecha_salida <= ? OR fecha_entrada >= ?)
        """, (numero_habitacion, fecha_entrada.strftime('%Y-%m-%d'), fecha_salida.strftime('%Y-%m-%d')))
        
        reservas = []
        for row in cursor.fetchall():
            reserva = Reserva(
                row['id'],
                row['numero_habitacion'],
                row['id_cliente'],
                datetime.datetime.strptime(row['fecha_entrada'], '%Y-%m-%d').date(),
                datetime.datetime.strptime(row['fecha_salida'], '%Y-%m-%d').date()
            )
            reservas.append(reserva)
        return reservas

# --- Lógica de Negocio de Calendario de Reservas ---

class CalendarioReservas:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def buscar_habitaciones_disponibles(self, fecha_entrada_str, fecha_salida_str, tipo_habitacion=None):
        try:
            fecha_entrada_dt = datetime.datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            fecha_salida_dt = datetime.datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
        except ValueError:
            return [], "Formato de fecha incorrecto. Use YYYY-MM-DD."

        if fecha_entrada_dt >= fecha_salida_dt:
            return [], "La fecha de entrada debe ser anterior a la fecha de salida."
        
        if fecha_entrada_dt < datetime.date.today():
            return [], "No se pueden buscar habitaciones con fechas de entrada pasadas."

        todas_habitaciones = self.db_manager.get_all_habitaciones()
        disponibles = []

        if not todas_habitaciones:
            return [], "No hay habitaciones registradas en el sistema. Por favor, registre habitaciones primero."

        for habitacion in todas_habitaciones:
            if tipo_habitacion and habitacion.tipo != tipo_habitacion:
                continue

            reservas_solapadas = self.db_manager.get_reservas_for_habitacion_and_period(
                habitacion.numero, fecha_entrada_dt, fecha_salida_dt
            )
            
            if not reservas_solapadas:
                disponibles.append(habitacion)
        return disponibles, ""

    def hacer_reserva(self, numero_habitacion_str, id_cliente_str, fecha_entrada_str, fecha_salida_str):
        try:
            num_hab_int = int(numero_habitacion_str)
            id_cliente_int = int(id_cliente_str)
        except ValueError:
            return False, "Número de habitación o ID de cliente inválido."

        habitacion_existe = self.db_manager.get_habitacion_by_numero(num_hab_int)
        if not habitacion_existe:
            return False, f"La habitación {num_hab_int} no existe en el sistema. Verifique con el módulo de habitaciones."
        
        cliente_existe = self.db_manager.get_cliente_by_id(id_cliente_int)
        if not cliente_existe:
            return False, f"El cliente con ID {id_cliente_int} no existe en el sistema. Verifique con el módulo de clientes."

        try:
            fecha_entrada_dt = datetime.datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            fecha_salida_dt = datetime.datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
        except ValueError:
            return False, "Formato de fecha incorrecto. Use YYYY-MM-DD."

        if fecha_entrada_dt >= fecha_salida_dt:
            return False, "La fecha de entrada debe ser anterior a la fecha de salida."
        
        if fecha_entrada_dt < datetime.date.today():
            return False, "No se pueden hacer reservas en el pasado."

        reservas_existentes = self.db_manager.get_reservas_for_habitacion_and_period(num_hab_int, fecha_entrada_dt, fecha_salida_dt)
        if reservas_existentes:
            return False, f"La habitación {num_hab_int} no está disponible entre {fecha_entrada_str} y {fecha_salida_str}."

        nueva_reserva = Reserva(None, num_hab_int, id_cliente_int, fecha_entrada_dt, fecha_salida_dt)
        exito, new_id, mensaje = self.db_manager.insert_reserva(nueva_reserva)
        if exito:
            nueva_reserva.id = new_id
            return True, f"Reserva {nueva_reserva.id} para la habitación {num_hab_int} realizada exitosamente."
        else:
            return False, mensaje

    def cancelar_reserva(self, id_reserva_str):
        try:
            id_reserva_int = int(id_reserva_str)
        except ValueError:
            return False, "El ID de reserva debe ser un número entero."
        
        exito = self.db_manager.delete_reserva(id_reserva_int)
        if exito:
            return True, f"Reserva {id_reserva_int} cancelada exitosamente."
        else:
            return False, f"No se encontró la reserva con ID {id_reserva_int}."

    def get_all_reservas_detalle(self):
        return self.db_manager.get_all_reservas()

# --- Interfaz Gráfica---

class CalendarioReservasApp(ttk.Frame): #convertido a frame para integración
    def __init__(self, root):
        super().__init__(root, width=900, height=700)
        self.db_manager = DatabaseManager() # Instancia el gestor de la DB
        self.calendario_reservas = CalendarioReservas(self.db_manager)

        self.ui_initialized = False #JSS: ni idea que hace esto, pregunten a google
        
        self.root = root
        # self.root.title("Módulo de Calendario de Reservas ")
        # self.root.geometry("900x700")

        # self.setup_ui() JS: se colocó en main.py
        
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # def on_closing(self):
    #     if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
    #         self.db_manager.close()
    #         self.root.destroy()

    def setup_ui(self):
        if self.ui_initialized:
            return #JSS: vuelvo y repito, busquen en google que no se

        self.notebook = ttk.Notebook(self) #JSS: modificado pa la integracion
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.frame_buscar_reservar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_buscar_reservar, text="Buscar y Reservar")
        self.create_buscar_reservar_tab(self.frame_buscar_reservar)

        self.frame_ver_cancelar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ver_cancelar, text="Ver y Cancelar Reservas")
        self.create_ver_cancelar_tab(self.frame_ver_cancelar)
        
        # Al inicio, o cuando la pestaña de clientes es seleccionada, refrescar los clientes
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.ui_initialized = True #JSS: esto es magia negra

    def on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Buscar y Reservar":
            self.populate_clientes_combo() # para asegurar que le  combobox de clientes esté actualizado

    def create_buscar_reservar_tab(self, parent_frame):
        search_frame = ttk.LabelFrame(parent_frame, text="Buscar Habitaciones Disponibles")
        search_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(search_frame, text="Fecha Entrada:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry_search_fecha_entrada = DateEntry(search_frame, width=12, background='darkblue',
                                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry_search_fecha_entrada.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Fecha Salida:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.date_entry_search_fecha_salida = DateEntry(search_frame, width=12, background='darkblue',
                                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry_search_fecha_salida.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Tipo de Habitación:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_search_tipo_habitacion = ttk.Combobox(search_frame, values=["", "Individual", "Doble", "Suite"])
        self.combo_search_tipo_habitacion.set("")
        self.combo_search_tipo_habitacion.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(search_frame, text="Buscar Disponibilidad", command=self.buscar_habitaciones).grid(row=3, column=0, columnspan=2, pady=10)

        self.listbox_habitaciones_disponibles = tk.Listbox(parent_frame, height=8, width=50)
        self.listbox_habitaciones_disponibles.pack(padx=10, pady=5, fill="both", expand=True)

        reserve_frame = ttk.LabelFrame(parent_frame, text="Hacer Nueva Reserva")
        reserve_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(reserve_frame, text="Número Habitación:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_reserve_num_hab = ttk.Entry(reserve_frame)
        self.entry_reserve_num_hab.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(reserve_frame, text="ID Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_reserve_id_cliente = ttk.Entry(reserve_frame)
        self.entry_reserve_id_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(reserve_frame, text="Clientes Existentes:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_clientes = ttk.Combobox(reserve_frame, state="readonly")
        self.combo_clientes.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.combo_clientes.bind("<<ComboboxSelected>>", self.seleccionar_cliente_para_reserva)
        self.populate_clientes_combo() # Cargar clientes al inicio de la pestaña

        ttk.Label(reserve_frame, text="Fecha Entrada (reserva):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.date_entry_reserve_fecha_entrada = DateEntry(reserve_frame, width=12, background='darkblue',
                                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry_reserve_fecha_entrada.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(reserve_frame, text="Fecha Salida (reserva):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.date_entry_reserve_fecha_salida = DateEntry(reserve_frame, width=12, background='darkblue',
                                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry_reserve_fecha_salida.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(reserve_frame, text="Confirmar Reserva", command=self.hacer_reserva).grid(row=5, column=0, columnspan=2, pady=10)

        #JSS: Aquí agrego el botón de Atrás
        ttk.Button(reserve_frame, text="Atrás", command=self.root.atras_reservas).place(relx=0.85, rely=0.9, anchor="center")

        

    def create_ver_cancelar_tab(self, parent_frame):
        all_reservations_frame = ttk.LabelFrame(parent_frame, text="Todas las Reservas")
        all_reservations_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.listbox_todas_reservas = tk.Listbox(all_reservations_frame, height=15)
        self.listbox_todas_reservas.pack(padx=5, pady=5, fill="both", expand=True)
        self.refresh_reservas_listbox()

        cancel_reservation_frame = ttk.LabelFrame(parent_frame, text="Cancelar Reserva")
        cancel_reservation_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(cancel_reservation_frame, text="ID Reserva:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_cancel_id_reserva = ttk.Entry(cancel_reservation_frame)
        self.entry_cancel_id_reserva.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(cancel_reservation_frame, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(all_reservations_frame, text="Actualizar Lista", command=self.refresh_reservas_listbox).pack(pady=5)

        #JSS: Aquí agrego el botón de Atrás
        ttk.Button(cancel_reservation_frame, text="Atrás", command=self.root.atras_reservas).place(relx=0.85, rely=0.7, anchor="center")

    def populate_clientes_combo(self):
        clientes = self.db_manager.get_all_clientes()
        self.clientes_map = {f"ID {c.id}: {c.nombre} ({c.email})": c.id for c in clientes}
        
        if not clientes:
            self.combo_clientes['values'] = ["No hay clientes registrados"]
            self.combo_clientes.set("No hay clientes registrados")
            self.combo_clientes.config(state="disabled") # Deshabilitar si no hay clientes
            self.entry_reserve_id_cliente.delete(0, tk.END)
        else:
            self.combo_clientes['values'] = list(self.clientes_map.keys())
            self.combo_clientes.set(list(self.clientes_map.keys())[0])
            self.combo_clientes.config(state="readonly")
            self.entry_reserve_id_cliente.delete(0, tk.END)
            self.entry_reserve_id_cliente.insert(0, str(clientes[0].id)) # Selecciona el ID del primer cliente por defecto

    def seleccionar_cliente_para_reserva(self, event=None):
        selected_text = self.combo_clientes.get()
        if selected_text in self.clientes_map:
            client_id = self.clientes_map[selected_text]
            self.entry_reserve_id_cliente.delete(0, tk.END)
            self.entry_reserve_id_cliente.insert(0, str(client_id))

    def buscar_habitaciones(self):
        fecha_entrada_dt = self.date_entry_search_fecha_entrada.get_date()
        fecha_salida_dt = self.date_entry_search_fecha_salida.get_date()
        tipo = self.combo_search_tipo_habitacion.get()

        fecha_entrada_str = fecha_entrada_dt.strftime('%Y-%m-%d')
        fecha_salida_str = fecha_salida_dt.strftime('%Y-%m-%d')

        disponibles, mensaje = self.calendario_reservas.buscar_habitaciones_disponibles(fecha_entrada_str, fecha_salida_str, tipo if tipo else None)
        
        self.listbox_habitaciones_disponibles.delete(0, tk.END)

        if mensaje:
            messagebox.showerror("Error de Búsqueda", mensaje)
            return

        if disponibles:
            for hab in disponibles:
                self.listbox_habitaciones_disponibles.insert(tk.END, str(hab))
            messagebox.showinfo("Búsqueda Exitosa", f"Se encontraron {len(disponibles)} habitaciones disponibles.")
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron habitaciones disponibles para los criterios dados o no hay habitaciones registradas.")

    def hacer_reserva(self):
        num_habitacion = self.entry_reserve_num_hab.get()
        id_cliente = self.entry_reserve_id_cliente.get()
        fecha_entrada_dt = self.date_entry_reserve_fecha_entrada.get_date()
        fecha_salida_dt = self.date_entry_reserve_fecha_salida.get_date()

        fecha_entrada_str = fecha_entrada_dt.strftime('%Y-%m-%d')
        fecha_salida_str = fecha_salida_dt.strftime('%Y-%m-%d')

        if not all([num_habitacion, id_cliente, fecha_entrada_str, fecha_salida_str]):
            messagebox.showwarning("Advertencia", "Todos los campos de reserva son obligatorios.")
            return

        exito, mensaje = self.calendario_reservas.hacer_reserva(num_habitacion, id_cliente, fecha_entrada_str, fecha_salida_str)
        
        if exito:
            messagebox.showinfo("Reserva Exitosa", mensaje)
            self.clear_reserve_entries()
            self.refresh_reservas_listbox()
        else:
            messagebox.showerror("Error de Reserva", mensaje)

    def cancelar_reserva(self):
        id_reserva = self.entry_cancel_id_reserva.get()

        if not id_reserva:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID de la reserva a cancelar.")
            return
        
        if not messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de cancelar la reserva con ID {id_reserva}?"):
            return

        exito, mensaje = self.calendario_reservas.cancelar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Cancelación Exitosa", mensaje)
            self.entry_cancel_id_reserva.delete(0, tk.END)
            self.refresh_reservas_listbox()
        else:
            messagebox.showerror("Error de Cancelación", mensaje)

    def refresh_reservas_listbox(self):
        self.listbox_todas_reservas.delete(0, tk.END)
        reservas_detalle = self.calendario_reservas.get_all_reservas_detalle()
        if reservas_detalle:
            for r in reservas_detalle:
                display_text = (f"ID: {r['id']} | Hab: {r['numero_habitacion']} ({r['tipo_habitacion']}) | "
                                f"Cliente: {r['nombre_cliente']} (ID: {r['id_cliente']}) | "
                                f"Entrada: {r['fecha_entrada'].strftime('%Y-%m-%d')} | "
                                f"Salida: {r['fecha_salida'].strftime('%Y-%m-%d')} | "
                                f"Costo/noche: ${r['precio_por_noche']:.2f}")
                self.listbox_todas_reservas.insert(tk.END, display_text)
        else:
            self.listbox_todas_reservas.insert(tk.END, "No hay reservas actualmente.")

    def clear_reserve_entries(self):
        self.entry_reserve_num_hab.delete(0, tk.END)
       
        


if __name__ == "__main__":
    
    root = tk.Tk()
    app = CalendarioReservasApp(root)
    root.mainloop()