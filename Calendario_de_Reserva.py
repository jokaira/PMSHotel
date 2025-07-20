import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from gestor_clientes import GestorClientes
import customtkinter as ctk

class CalendarioReservasApp(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.db_manager = DatabaseManager()
        self.calendario_reservas = CalendarioReservas(self.db_manager)
        self.ui_initialized = False
        self.root = root
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", 
                           foreground="white", 
                           background="#c0392b", 
                           font=("Arial", 11, "bold"),
                           padding=(15, 8))
        self.style.map("TButton",
            background=[("active", "#e74c3c"), ("pressed", "#a93226")],
            foreground=[("active", "#fff")]
        )
        self.style.configure("Treeview.Heading", 
                           background="#c0392b", 
                           foreground="white", 
                           font=("Arial", 10, "bold"))
        self.style.configure("Treeview", 
                           background="#fff", 
                           fieldbackground="#fff", 
                           font=("Arial", 9),
                           rowheight=25)
        
        # Main layout
        self.create_layout()
    
    def create_layout(self):
        """Create the main layout structure"""
        # Header section
        self.create_header()
        
        # Main content area
        self.create_main_content()
    
    def create_header(self):
        """Create the header with title and back button"""
        header_frame = ctk.CTkFrame(self, fg_color="#c0392b", corner_radius=10, height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="📅 Gestor de Reservas", 
            font=("Arial", 20, "bold"), 
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Volver al Dashboard",
            fg_color="transparent",
            text_color="white",
            font=("Arial", 12, "bold"),
            hover_color="#e74c3c",
            command=self.go_back
        )
        back_btn.pack(side="right", padx=20, pady=15)
    
    def create_main_content(self):
        """Create the main content area with notebook"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Create notebook
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(expand=True, fill="both")
        
        # Create tabs
        self.create_search_reserve_tab()
        self.create_view_cancel_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.ui_initialized = True
    
    def create_search_reserve_tab(self):
        """Create the search and reserve tab"""
        self.tab_search = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(self.tab_search, text="🔍 Buscar y Reservar")
        
        # Search section
        self.create_search_section()
        
        # Available rooms section
        self.create_available_rooms_section()
        
        # Reservation section
        self.create_reservation_section()
    
    def create_search_section(self):
        """Create the search section"""
        search_frame = ctk.CTkFrame(self.tab_search, fg_color="#f8f9fa", corner_radius=10)
        search_frame.pack(fill="x")
        
        # Section title
        title_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar Habitaciones Disponibles",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=5)
        
        # Search form
        form_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Date inputs
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=10)
        
        # Check-in date
        checkin_label = ctk.CTkLabel(
            date_frame,
            text="📅 Fecha de Entrada:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        checkin_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.date_entry_search_fecha_entrada = DateEntry(
            date_frame, 
            width=15, 
            date_pattern='yyyy-mm-dd',
            font=("Arial", 11)
        )
        self.date_entry_search_fecha_entrada.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")
        
        # Check-out date
        checkout_label = ctk.CTkLabel(
            date_frame,
            text="📅 Fecha de Salida:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        checkout_label.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")
        
        self.date_entry_search_fecha_salida = DateEntry(
            date_frame, 
            width=15, 
            date_pattern='yyyy-mm-dd',
            font=("Arial", 11)
        )
        self.date_entry_search_fecha_salida.grid(row=0, column=3, padx=(0, 20), pady=5, sticky="w")
        
        # Room type filter
        type_label = ctk.CTkLabel(
            date_frame,
            text="🏠 Tipo de Habitación:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        type_label.grid(row=0, column=4, padx=(0, 10), pady=5, sticky="w")
        
        self.combo_search_tipo_habitacion = ttk.Combobox(
            date_frame,
            values=["", "Individual", "Doble", "Suite"],
            state="readonly",
            font=("Arial", 11),
            width=12
        )
        self.combo_search_tipo_habitacion.set("")
        self.combo_search_tipo_habitacion.grid(row=0, column=5, padx=(0, 20), pady=5, sticky="w")
        
        # Search button
        search_btn = ctk.CTkButton(
            date_frame,
            text="🔍 Buscar Disponibilidad",
            fg_color="#3498db",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=35,
            command=self.buscar_habitaciones
        )
        search_btn.grid(row=0, column=6, padx=(0, 0), pady=5)
    
    def create_available_rooms_section(self):
        """Create the available rooms display section"""
        rooms_frame = ctk.CTkFrame(self.tab_search, fg_color="#f8f9fa", corner_radius=10)
        rooms_frame.pack(fill="both", expand=True)
        
        # Section title
        title_label = ctk.CTkLabel(
            rooms_frame,
            text="🏠 Habitaciones Disponibles",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=5)
        
        # Rooms list
        self.listbox_habitaciones_disponibles = ctk.CTkTextbox(
            rooms_frame, 
            height=50, 
            fg_color="white", 
            border_color="#bdc3c7", 
            border_width=2, 
            font=("Arial", 11)
        )
        self.listbox_habitaciones_disponibles.pack(fill="both", expand=True, padx=20, pady=5)
    
    def create_reservation_section(self):
        """Create the reservation form section"""
        reserve_frame = ctk.CTkFrame(self.tab_search, fg_color="#f8f9fa", corner_radius=10)
        reserve_frame.pack(fill="x")
        
        # Section title
        title_label = ctk.CTkLabel(
            reserve_frame,
            text="📝 Hacer Nueva Reserva",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=(15, 20))
        
        # Reservation form
        form_frame = ctk.CTkFrame(reserve_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # First row
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        # Room number
        room_label = ctk.CTkLabel(
            row1,
            text="🏠 Número Habitación:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        room_label.pack(side="left", padx=(0, 10))
        
        self.entry_reserve_num_hab = ctk.CTkEntry(
            row1,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=2,
            font=("Arial", 11),
            width=150
        )
        self.entry_reserve_num_hab.pack(side="left", padx=(0, 30))
        
        # Client ID
        client_id_label = ctk.CTkLabel(
            row1,
            text="👤 ID Cliente:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        client_id_label.pack(side="left", padx=(0, 10))
        
        self.entry_reserve_id_cliente = ctk.CTkEntry(
            row1,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=2,
            font=("Arial", 11),
            width=100
        )
        self.entry_reserve_id_cliente.pack(side="left")
        
        # Second row
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        # Client selection
        client_label = ctk.CTkLabel(
            row2,
            text="👥 Cliente:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        client_label.pack(side="left", padx=(0, 10))
        
        self.combo_clientes = ttk.Combobox(
            row2,
            state="readonly",
            font=("Arial", 11),
            width=40
        )
        self.combo_clientes.pack(side="left", padx=(0, 30))
        self.combo_clientes.bind("<<ComboboxSelected>>", self.seleccionar_cliente_para_reserva)
        
        # Third row
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        
        # Check-in date
        checkin_reserve_label = ctk.CTkLabel(
            row3,
            text="📅 Fecha Entrada:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        checkin_reserve_label.pack(side="left", padx=(0, 10))
        
        self.date_entry_reserve_fecha_entrada = DateEntry(
            row3, 
            width=15, 
            date_pattern='yyyy-mm-dd',
            font=("Arial", 11)
        )
        self.date_entry_reserve_fecha_entrada.pack(side="left", padx=(0, 30))
        
        # Check-out date
        checkout_reserve_label = ctk.CTkLabel(
            row3,
            text="📅 Fecha Salida:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        checkout_reserve_label.pack(side="left", padx=(0, 10))
        
        self.date_entry_reserve_fecha_salida = DateEntry(
            row3, 
            width=15, 
            date_pattern='yyyy-mm-dd',
            font=("Arial", 11)
        )
        self.date_entry_reserve_fecha_salida.pack(side="left")
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            form_frame,
            text="✅ Confirmar Reserva",
            fg_color="#27ae60",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.hacer_reserva
        )
        confirm_btn.pack(pady=15)
    
    def create_view_cancel_tab(self):
        """Create the view and cancel reservations tab"""
        self.tab_view = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(self.tab_view, text="📋 Ver y Cancelar Reservas")
        
        # All reservations section
        self.create_all_reservations_section()
        
        # Cancel reservation section
        self.create_cancel_reservation_section()
    
    def create_all_reservations_section(self):
        """Create the all reservations display section"""
        reservations_frame = ctk.CTkFrame(self.tab_view, fg_color="#f8f9fa", corner_radius=10)
        reservations_frame.pack(fill="both", expand=True)
        
        # Section title
        title_label = ctk.CTkLabel(
            reservations_frame,
            text="📋 Todas las Reservas",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=(15, 10))
        
        # Reservations list
        self.listbox_todas_reservas = ctk.CTkTextbox(
            reservations_frame, 
            height=100, 
            fg_color="white", 
            border_color="#bdc3c7", 
            border_width=2, 
            font=("Arial", 11)
        )
        self.listbox_todas_reservas.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            reservations_frame,
            text="🔄 Actualizar Lista",
            fg_color="#3498db",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=35,
            command=self.refresh_reservas_listbox
        )
        refresh_btn.pack(pady=(0, 15))
    
    def create_cancel_reservation_section(self):
        """Create the cancel reservation section"""
        cancel_frame = ctk.CTkFrame(self.tab_view, fg_color="#f8f9fa", corner_radius=10)
        cancel_frame.pack(fill="x")
        
        # Section title
        title_label = ctk.CTkLabel(
            cancel_frame,
            text="❌ Cancelar Reserva",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=(15, 20))
        
        # Cancel form
        form_frame = ctk.CTkFrame(cancel_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Reservation ID
        id_label = ctk.CTkLabel(
            form_frame,
            text="🆔 ID Reserva:",
            font=("Arial", 12, "bold"),
            text_color="#2c3e50"
        )
        id_label.pack(side="left", padx=(0, 10))
        
        self.entry_cancel_id_reserva = ctk.CTkEntry(
            form_frame,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=2,
            font=("Arial", 11),
            width=150
        )
        self.entry_cancel_id_reserva.pack(side="left", padx=(0, 20))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            form_frame,
            text="❌ Cancelar Reserva",
            fg_color="#e74c3c",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=35,
            command=self.cancelar_reserva
        )
        cancel_btn.pack(side="left")

    def on_tab_change(self, event):
        """Handle tab change events"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "🔍 Buscar y Reservar":
            self.populate_clientes_combo()
    
    def setup_ui(self):
        """Setup the UI (called from main)"""
        if not self.ui_initialized:
            self.create_main_content()
    
    # Rest of the methods remain the same but with updated styling
    def populate_clientes_combo(self):
        """Populate the clients combobox"""
        clientes = self.db_manager.get_all_clientes()
        self.clientes_map = {f"ID {c.id}: {c.nombre} ({c.email})": c.id for c in clientes}
        
        if not clientes:
            self.combo_clientes['values'] = ["No hay clientes registrados"]
            self.combo_clientes.set("No hay clientes registrados")
            self.combo_clientes.config(state="disabled")
            self.entry_reserve_id_cliente.delete(0, tk.END)
        else:
            self.combo_clientes['values'] = list(self.clientes_map.keys())
            self.combo_clientes.set(list(self.clientes_map.keys())[0])
            self.combo_clientes.config(state="readonly")
            self.entry_reserve_id_cliente.delete(0, tk.END)
            self.entry_reserve_id_cliente.insert(0, str(clientes[0].id))

    def seleccionar_cliente_para_reserva(self, event=None):
        """Handle client selection for reservation"""
        selected_text = self.combo_clientes.get()
        if selected_text in self.clientes_map:
            client_id = self.clientes_map[selected_text]
            self.entry_reserve_id_cliente.delete(0, tk.END)
            self.entry_reserve_id_cliente.insert(0, str(client_id))

    def buscar_habitaciones(self):
        """Search for available rooms"""
        fecha_entrada_dt = self.date_entry_search_fecha_entrada.get_date()
        fecha_salida_dt = self.date_entry_search_fecha_salida.get_date()
        tipo = self.combo_search_tipo_habitacion.get()

        fecha_entrada_str = fecha_entrada_dt.strftime('%Y-%m-%d')
        fecha_salida_str = fecha_salida_dt.strftime('%Y-%m-%d')

        disponibles, mensaje = self.calendario_reservas.buscar_habitaciones_disponibles(
            fecha_entrada_str, fecha_salida_str, tipo if tipo else None
        )
        
        self.listbox_habitaciones_disponibles.delete("1.0", tk.END)

        if mensaje:
            messagebox.showerror("Error de Búsqueda", mensaje)
            return

        if disponibles:
            for hab in disponibles:
                self.listbox_habitaciones_disponibles.insert(tk.END, str(hab) + "\n")
            messagebox.showinfo("Búsqueda Exitosa", f"Se encontraron {len(disponibles)} habitaciones disponibles.")
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron habitaciones disponibles para los criterios dados.")

    def hacer_reserva(self):
        """Make a reservation"""
        num_habitacion = self.entry_reserve_num_hab.get()
        id_cliente = self.entry_reserve_id_cliente.get()
        fecha_entrada_dt = self.date_entry_reserve_fecha_entrada.get_date()
        fecha_salida_dt = self.date_entry_reserve_fecha_salida.get_date()

        fecha_entrada_str = fecha_entrada_dt.strftime('%Y-%m-%d')
        fecha_salida_str = fecha_salida_dt.strftime('%Y-%m-%d')

        if not all([num_habitacion, id_cliente, fecha_entrada_str, fecha_salida_str]):
            messagebox.showwarning("Advertencia", "Todos los campos de reserva son obligatorios.")
            return

        exito, mensaje = self.calendario_reservas.hacer_reserva(
            num_habitacion, id_cliente, fecha_entrada_str, fecha_salida_str
        )
        
        if exito:
            messagebox.showinfo("Reserva Exitosa", mensaje)
            self.clear_reserve_entries()
            self.refresh_reservas_listbox()
        else:
            messagebox.showerror("Error de Reserva", mensaje)

    def cancelar_reserva(self):
        """Cancel a reservation"""
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
        """Refresh the reservations list"""
        self.listbox_todas_reservas.delete("1.0", tk.END)
        reservas_detalle = self.calendario_reservas.get_all_reservas_detalle()
        if reservas_detalle:
            for reserva in reservas_detalle:
                self.listbox_todas_reservas.insert(tk.END, str(reserva) + "\n")
        else:
            self.listbox_todas_reservas.insert(tk.END, "No hay reservas registradas.")

    def clear_reserve_entries(self):
        """Clear reservation form entries"""
        self.entry_reserve_num_hab.delete(0, tk.END)
        self.entry_reserve_id_cliente.delete(0, tk.END)

    def go_back(self):
        """
        Función para regresar al dashboard principal.
        Busca el widget padre que tenga el método atras_reservas y lo ejecuta.
        """
        # Busca el widget padre que tenga el método atras_reservas
        parent = self.master  # Obtiene el widget padre
        while parent:  # Mientras exista un widget padre
            if hasattr(parent, 'atras_reservas'):  # Verifica si tiene el método
                parent.atras_reservas()  # Ejecuta el método
                break  # Sale del bucle
            parent = parent.master  # Obtiene el siguiente widget padre

# Keep the existing database classes (DatabaseManager, Cliente, Habitacion, CalendarioReservas) as they are
# since they handle the business logic and don't need UI restructuring

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

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarioReservasApp(root)
    root.mainloop()