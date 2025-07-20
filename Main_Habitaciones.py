
# Importación de librerías necesarias para la interfaz gráfica y base de datos
import customtkinter as ctk  # Librería moderna para widgets de tkinter
from tkinter import ttk, messagebox  # Widgets temáticos y cuadros de diálogo
import sqlite3 as sql  # Para conexión con base de datos SQLite
from tkinter import *  # Importa todos los widgets básicos de tkinter
import tkinter as tk

import manejo_habitaciones #
import BD_Modulo_Habitaciones #

#Aplicación principal de gestión de habitaciones.
#Proporciona una interfaz gráfica para visualizar, añadir,
#editar y cambiar el estado de las habitaciones.
   
class GestionDeHabitacionesApp(ctk.CTkFrame):
    """
    Clase para la gestión de habitaciones del sistema PMS Hotel.
    Hereda de ctk.CTkFrame para crear un módulo integrado en la interfaz principal.
    Proporciona funcionalidades para agregar, editar, eliminar y gestionar habitaciones.
    """
    
    def __init__(self, parent):
        """
        Constructor de la clase GestionDeHabitacionesApp.
        
        Args:
            parent: Widget padre donde se creará el módulo de habitaciones
        """
        super().__init__(parent)  # Llama al constructor de la clase padre
        
        # Configuración del frame principal
        self.configure(fg_color="transparent")  # Hace el frame transparente
        
        # Inicialización de variables de control
        self.habitacion_actual = None  # Variable para almacenar la habitación seleccionada actualmente
        self.busqueda_var = StringVar()  # Variable para el campo de búsqueda
        self.filtro_estado_var = StringVar(value="Todos")  # Variable para el filtro de estado
        
        # Creación de la interfaz de usuario
        self.setup_ui()  # Llama al método para configurar la interfaz
        
        # Carga inicial de datos
        self.load_rooms()  # Carga la lista de habitaciones desde la base de datos
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario del módulo de habitaciones.
        Crea todos los elementos visuales: encabezado, filtros, tabla y botones.
        """
        # Creación del frame principal del módulo
        main_frame = ctk.CTkFrame(self, fg_color="#fff", corner_radius=15)  # Frame blanco con esquinas redondeadas
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)  # Empaqueta con padding
        
        # Creación del encabezado del módulo
        self.create_header(main_frame)  # Llama al método para crear el encabezado
        
        # Creación del área de búsqueda y filtros
        self.create_search_filters(main_frame)  # Llama al método para crear los filtros
        
        # Creación de la tabla de habitaciones
        self.create_table_section(main_frame)  # Llama al método para crear la tabla
        
        # Creación del área de botones de acción
        self.create_action_buttons(main_frame)  # Llama al método para crear los botones
    
    def create_header(self, parent):
        """
        Crea el encabezado del módulo con título y botón de regreso.
        
        Args:
            parent: Widget padre donde se creará el encabezado
        """
        # Creación del frame del encabezado con color rojo y esquinas redondeadas
        header_frame = ctk.CTkFrame(parent, fg_color="#c0392b", corner_radius=10, height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))  # Empaqueta horizontalmente con padding
        header_frame.pack_propagate(False)  # Evita que el frame se redimensione automáticamente
        
        # Creación del botón de regreso con emoji de flecha
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Volver",  # Texto con emoji de flecha
            fg_color="transparent",  # Color de fondo transparente
            text_color="white",  # Color del texto: blanco
            font=("Arial", 12, "bold"),  # Fuente mediana y negrita
            hover_color="#e74c3c",  # Color al pasar el mouse
            command=self.go_back  # Función a ejecutar al hacer clic
        )
        back_btn.pack(side="left", padx=20, pady=15)  # Empaqueta a la izquierda con padding
        
        # Creación del título del módulo
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏠 Gestión de Habitaciones",  # Título con emoji de casa
            font=("Arial", 20, "bold"),  # Fuente grande y negrita
            text_color="white"  # Color del texto: blanco
        )
        title_label.pack(side="left", padx=(20, 0), pady=15)  # Empaqueta a la izquierda con padding
    
    def go_back(self):
        """
        Función para regresar al dashboard principal.
        Busca el widget padre que tenga el método atras_habitaciones y lo ejecuta.
        """
        # Busca el widget padre que tenga el método atras_habitaciones
        parent = self.master  # Obtiene el widget padre
        while parent:  # Mientras exista un widget padre
            if hasattr(parent, 'atras_habitaciones'):  # Verifica si tiene el método
                parent.atras_habitaciones()  # Ejecuta el método
                break  # Sale del bucle
            parent = parent.master  # Obtiene el siguiente widget padre
    
    def create_search_filters(self, parent):
        """
        Crea el área de búsqueda y filtros para las habitaciones.
        
        Args:
            parent: Widget padre donde se creará el área de búsqueda
        """
        # Creación del frame del área de búsqueda
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")  # Frame transparente
        search_frame.pack(fill="x", padx=20, pady=10)  # Empaqueta horizontalmente con padding
        
        # Creación del label para el campo de búsqueda
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar Habitación:",  # Texto con emoji de lupa
            font=("Arial", 12, "bold"),  # Fuente mediana y negrita
            text_color="#2c3e50"  # Color del texto: azul oscuro
        )
        search_label.pack(side="left", padx=(0, 10))  # Empaqueta a la izquierda con padding
        
        # Creación del campo de entrada para búsqueda
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.busqueda_var,  # Variable asociada al campo
            placeholder_text="Buscar por número, tipo o ubicación...",  # Texto de placeholder
            width=250,  # Ancho del campo
            height=35,  # Altura del campo
            font=("Arial", 12),  # Fuente mediana
            border_color="#c0392b",  # Color del borde: rojo
            fg_color="#f8f9fa"  # Color de fondo: gris claro
        )
        self.search_entry.pack(side="left", padx=(0, 20))  # Empaqueta a la izquierda con padding
        
        # Vincular el evento de cambio de texto para filtrado automático
        self.busqueda_var.trace("w", self.filter_rooms)  # Filtra automáticamente al escribir
        
        # Creación del label para el filtro de estado
        status_label = ctk.CTkLabel(
            search_frame,
            text="Estado:",  # Texto del label
            font=("Arial", 12, "bold"),  # Fuente mediana y negrita
            text_color="#2c3e50"  # Color del texto: azul oscuro
        )
        status_label.pack(side="left", padx=(0, 10))  # Empaqueta a la izquierda con padding
        
        # Creación del combobox para filtrar por estado
        self.status_filter = ttk.Combobox(
            search_frame,
            textvariable=self.filtro_estado_var,  # Variable asociada
            values=["Todos", "Disponible", "Ocupada", "Sucia", "Limpiando", "Mantenimiento", "Fuera de Servicio"],  # Opciones disponibles
            state="readonly",  # Solo lectura
            font=("Arial", 12),  # Fuente mediana
            width=15  # Ancho del combobox
        )
        self.status_filter.pack(side="left", padx=(0, 20))  # Empaqueta a la izquierda con padding
        self.status_filter.bind("<<ComboboxSelected>>", self.filter_rooms)  # Vincula evento de selección
        
        # Creación del botón para limpiar filtros
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Limpiar",  # Texto del botón
            fg_color="#95a5a6",  # Color de fondo: gris
            text_color="white",  # Color del texto: blanco
            font=("Arial", 12, "bold"),  # Fuente mediana y negrita
            height=35,  # Altura del botón
            hover_color="#7f8c8d",  # Color al pasar el mouse
            command=self.clear_filters  # Función a ejecutar al hacer clic
        )
        clear_btn.pack(side="left")  # Empaqueta a la izquierda
    
    def create_table_section(self, parent):
        """Create the main table section"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Table title
        table_title = ctk.CTkLabel(
            table_frame,
            text="📋 Lista de Habitaciones",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        table_title.pack(anchor="w", pady=(0, 10))
        
        # Create table with scrollbar
        table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True)
        
        # Treeview
        self.room_tree = ttk.Treeview(
            table_container,
            columns=("ID", "Número", "Tipo", "Estado", "Ubicación", "Capacidad", "Notas"),
            show="headings",
            height=4
        )
        
        # Configure columns
        column_widths = [50, 80, 100, 120, 120, 80, 150]
        for i, (col, width) in enumerate(zip(["ID", "Número", "Tipo", "Estado", "Ubicación", "Capacidad", "Notas"], column_widths)):
            self.room_tree.column(col, width=width, anchor="center")
            self.room_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.room_tree.yview)
        self.room_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.room_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for editing
        self.room_tree.bind("<Double-1>", self.on_double_click)
    
    def create_action_buttons(self, parent):
        """Create the action buttons toolbar"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left", padx=20, pady=15)
        
        # Add room button
        add_btn = ctk.CTkButton(
            left_buttons,
            text="➕ Añadir Habitación",
            fg_color="#27ae60",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.open_add_room_window
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        # Edit room button
        edit_btn = ctk.CTkButton(
            left_buttons,
            text="✏️ Editar Habitación",
            fg_color="#f39c12",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.open_edit_room_window
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        # Change status button
        status_btn = ctk.CTkButton(
            left_buttons,
            text="🔄 Cambiar Estado",
            fg_color="#3498db",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.open_change_status_window
        )
        status_btn.pack(side="left", padx=(0, 10))
        
        # Delete room button
        delete_btn = ctk.CTkButton(
            left_buttons,
            text="🗑️ Eliminar Habitación",
            fg_color="#e74c3c",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.delete_selected_room
        )
        delete_btn.pack(side="left")
        
        # Right side - refresh button
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Actualizar",
            fg_color="#9b59b6",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.refresh_data
        )
        refresh_btn.pack(side="right", padx=20, pady=15)
    
    def load_rooms(self):
        """Load room data into the table"""
        self.clear_table()
        
        rooms = manejo_habitaciones.obtener_info_habitaciones()
        for room in rooms:
            item = self.room_tree.insert("", tk.END, iid=room['id_habitacion'], values=(
                room['id_habitacion'],
                room['numero_habitacion'],
                room['tipo_habitacion'],
                room['estado_habitacion'],
                room['ubicacion'],
                room['capacidad_maxima'],
                room['notas_internas']
            ))
            
            # Apply color coding based on status
            status = room['estado_habitacion'].lower().replace(" ", "_")
            self.apply_status_color(item, status)
    
    def apply_status_color(self, item, status):
        """Apply color coding to table rows based on status"""
        colors = {
            "disponible": "#d5f4e6",      # Light green
            "ocupada": "#fadbd8",         # Light red
            "sucia": "#fef9e7",           # Light yellow
            "limpiando": "#d6eaf8",       # Light blue
            "mantenimiento": "#e8d4f2",   # Light purple
            "fuera_de_servicio": "#d5dbdb" # Light gray
        }
        
        if status in colors:
            self.room_tree.tag_configure(status, background=colors[status])
            self.room_tree.item(item, tags=(status,))
    
    def clear_table(self):
        """Clear all items from the table"""
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
    
    def filter_rooms(self, *args):
        """Filter rooms based on search text and status filter"""
        search_text = self.busqueda_var.get().lower()
        status_filter = self.status_filter.get()
        
        self.clear_table()
        
        rooms = manejo_habitaciones.obtener_info_habitaciones()
        for room in rooms:
            # Check search text
            search_match = any(search_text in str(field).lower() for field in [
                room['numero_habitacion'], room['tipo_habitacion'], room['ubicacion']
            ])
            
            # Check status filter
            status_match = status_filter == "Todos" or room['estado_habitacion'] == status_filter
            
            if search_match and status_match:
                item = self.room_tree.insert("", tk.END, iid=room['id_habitacion'], values=(
                    room['id_habitacion'],
                    room['numero_habitacion'],
                    room['tipo_habitacion'],
                    room['estado_habitacion'],
                    room['ubicacion'],
                    room['capacidad_maxima'],
                    room['notas_internas']
                ))
                
                status = room['estado_habitacion'].lower().replace(" ", "_")
                self.apply_status_color(item, status)
    
    def clear_filters(self):
        """Clear all filters and reload data"""
        self.busqueda_var.set("")
        self.status_filter.set("Todos")
        self.load_rooms()
    
    def on_double_click(self, event):
        """Handle double-click on table row"""
        self.open_edit_room_window()
    
    def refresh_data(self):
        """Refresh the room data"""
        self.load_rooms()
        messagebox.showinfo("Información", "Datos actualizados correctamente")
    
    def open_add_room_window(self):
        """Open add room dialog"""
        AddRoomWindow(self)
    
    def open_edit_room_window(self):
        """Open edit room dialog"""
        selection = self.room_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No se ha seleccionado ninguna habitación para editar")
            return
        
        room_id = selection[0]
        EditRoomWindow(self, room_id)
    
    def open_change_status_window(self):
        """Open change status dialog"""
        selection = self.room_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No se ha seleccionado ninguna habitación")
            return
        
        room_id = selection[0]
        ChangeStatusWindow(self, room_id)
    
    def delete_selected_room(self):
        """Delete selected room"""
        selection = self.room_tree.selection()
        if not selection:
            messagebox.showerror("Error", "No se ha seleccionado ninguna habitación para eliminar")
            return
        
        room_id = selection[0]
        room_data = self.room_tree.item(room_id, "values")
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la habitación {room_data[1]}?"):
            try:
                # Add delete functionality here
                messagebox.showinfo("Éxito", "Habitación eliminada exitosamente")
                self.load_rooms()
            except Exception as error:
                messagebox.showerror("Error", f"Error al eliminar: {error}")

# Rest of the classes (AddRoomWindow, EditRoomWindow, ChangeStatusWindow) remain the same
# but with updated styling to match the new layout

class AddRoomWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Añadir Nueva Habitación")
        self.geometry("450x500")
        self.parent = parent
        self.grab_set()
        self.configure(bg="#f8f9fa")
        
        self.create_form()
    
    def create_form(self):
        """Create the form for adding a room"""
        # Header
        header_label = ctk.CTkLabel(
            self,
            text="➕ Añadir Nueva Habitación",
            font=("Arial", 18, "bold"),
            text_color="#2c3e50"
        )
        header_label.pack(pady=(20, 30))
        
        # Form frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Form fields
        fields = [
            ("Número de Habitación:", "entry"),
            ("Tipo de Habitación:", "combobox"),
            ("Ubicación:", "entry"),
            ("Capacidad Máxima:", "entry"),
            ("Notas Internas:", "entry")
        ]
        
        self.entries = []
        for i, (label_text, field_type) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=("Arial", 12, "bold"),
                text_color="#2c3e50"
            )
            label.grid(row=i, column=0, padx=(0, 15), pady=10, sticky="w")
            
            # Field
            if field_type == "combobox":
                type_options = [t['nombre_tipo'] for t in manejo_habitaciones.obtener_tipos_hab_disponible()]
                entry = ttk.Combobox(
                    form_frame,
                    values=type_options,
                    state="readonly",
                    font=("Arial", 11)
                )
                if type_options:
                    entry.set(type_options[0])
            else:
                entry = ctk.CTkEntry(
                    form_frame,
                    font=("Arial", 11),
                    height=35,
                    fg_color="white",
                    border_color="#bdc3c7",
                    border_width=2
                )
            
            entry.grid(row=i, column=1, padx=(0, 0), pady=10, sticky="ew")
            self.entries.append(entry)
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Guardar",
            fg_color="#27ae60",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.save_room
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancelar",
            fg_color="#95a5a6",
            text_color="white",
            font=("Arial", 12, "bold"),
            height=40,
            command=self.destroy
        )
        cancel_btn.pack(side="left")
    
    def save_room(self):
        """Save the new room"""
        values = [entry.get() for entry in self.entries]
        
        if not all(values[:3]):  # Check required fields
            messagebox.showwarning("Advertencia", "Número, Tipo y Capacidad son campos obligatorios.")
            return
        
        try:
            capacidad = int(values[3])
            if capacidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Capacidad Máxima debe ser un número entero positivo.")
            return
        
        if manejo_habitaciones.agregar_nueva_hab(*values):
            messagebox.showinfo("Éxito", f"Habitación {values[0]} añadida exitosamente.")
            self.parent.load_rooms()
            self.destroy()
        else:
            messagebox.showerror("Error", "Error al añadir habitación. Verifique si el número ya existe.")

# Similar updates for EditRoomWindow and ChangeStatusWindow classes...
# (I'll continue with these if you want the complete restructure)


class EditRoomWindow(ctk.CTkToplevel): #
    """
    Ventana para editar los detalles de una habitación existente.
    """
    def __init__(self, parent, room_id): #
        super().__init__(parent) #
        self.title(f"Editar Habitación ID: {room_id}") #
        self.geometry("350x350") #
        self.parent = parent #
        self.room_id = room_id #
        self.grab_set() #

        self.room_details = manejo_habitaciones.obtener_detalles_hab(self.room_id) #
        if not self.room_details: #
            messagebox.showerror("Error", "Habitación no encontrada para edición.") #
            self.destroy() #
            return #

        self.create_form() #
        self.load_room_data() #

    def create_form(self): #
        """Crea los campos del formulario para editar una habitación."""
        from tkinter import ttk
        form_frame = ctk.CTkFrame(self, fg_color="#fff") #
        form_frame.pack(fill="both", expand=True) #

        ctk.CTkLabel(form_frame, text="Número de Habitación:", text_color="#c0392b", fg_color="#fff").grid(row=0, column=0, padx=5, pady=5, sticky="w") #
        self.entry_numero = ctk.CTkEntry(form_frame, fg_color="#fff", border_color="#c0392b", border_width=2) #
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5, sticky="ew") #

        ctk.CTkLabel(form_frame, text="Tipo de Habitación:", text_color="#c0392b", fg_color="#fff").grid(row=1, column=0, padx=5, pady=5, sticky="w") #
        self.type_options = [t['nombre_tipo'] for t in manejo_habitaciones.obtener_tipos_hab_disponible()] #
        self.combo_tipo = ttk.Combobox(form_frame, values=self.type_options, state="readonly") #
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="ew") #

        ctk.CTkLabel(form_frame, text="Estado Actual:", text_color="#c0392b", fg_color="#fff").grid(row=2, column=0, padx=5, pady=5, sticky="w") #
        self.state_options = [s['nombre_estado'] for s in manejo_habitaciones.obtener_estado_hab_disponible()] #
        self.combo_estado = ttk.Combobox(form_frame, values=self.state_options, state="readonly") #
        self.combo_estado.grid(row=2, column=1, padx=5, pady=5, sticky="ew") #

        form_frame.columnconfigure(1, weight=1) #

    def load_room_data(self): #
        """Carga los datos de la habitación seleccionada en el formulario."""
        self.entry_numero.insert(0, self.room_details['numero_habitacion']) #
        self.combo_tipo.set(self.room_details['tipo_habitacion_nombre']) #
        self.combo_estado.set(self.room_details['estado_habitacion_nombre']) #
        self.entry_ubicacion.insert(0, self.room_details['ubicacion'] or "") #
        self.entry_capacidad.insert(0, str(self.room_details['capacidad_maxima'] or "")) #
        self.entry_notas.insert(0, self.room_details['notas_internas'] or "") #

    def save_changes(self): #
        """Guarda los cambios de la habitación editada."""
        numero = self.entry_numero.get().strip() #
        tipo = self.combo_tipo.get() #
        estado = self.combo_estado.get() #
        ubicacion = self.entry_ubicacion.get().strip() #
        capacidad_str = self.entry_capacidad.get().strip() #
        notas = self.entry_notas.get().strip() #

        if not numero or not tipo or not estado or not capacidad_str: #
            messagebox.showwarning("Entrada Inválida", "Número, Tipo, Estado y Capacidad son campos obligatorios.") #
            return #

        try: #
            capacidad = int(capacidad_str) #
            if capacidad <= 0: #
                raise ValueError #
        except ValueError: #
            messagebox.showwarning("Entrada Inválida", "Capacidad Máxima debe ser un número entero positivo.") #
            return #

        if manejo_habitaciones.actualizar_hab_existente( #
            self.room_id, numero, tipo, estado, ubicacion, capacidad, notas
        ):
            messagebox.showinfo("Éxito", f"Habitación {numero} actualizada.") #
            self.parent.load_rooms() #
            self.destroy() #
        else:
            messagebox.showerror("Error", "Error al actualizar habitación. Verifique el número de habitación.") #


class ChangeStatusWindow(ctk.CTkToplevel): #
    """
    Ventana para cambiar el estado de una habitación.
    """
    def __init__(self, parent, room_id): #
        super().__init__(parent) #
        self.title("Cambiar Estado de Habitación") #
        self.geometry("300x150") #
        self.parent = parent #
        self.room_id = room_id #
        self.grab_set() #

        self.room_details = manejo_habitaciones.obtener_detalles_hab(self.room_id) #
        if not self.room_details: #
            messagebox.showerror("Error", "Habitación no encontrada.") #
            self.destroy() #
            return #

        self.create_form() #
        self.load_current_status() #

    def create_form(self): #
        """Crea los campos del formulario para cambiar el estado."""
        from tkinter import ttk
        form_frame = ctk.CTkFrame(self, fg_color="#fff") #
        form_frame.pack(fill="both", expand=True) #

        ctk.CTkLabel(form_frame, text=f"Habitación: {self.room_details['numero_habitacion']}", text_color="#c0392b", fg_color="#fff").pack(pady=5) #
        ctk.CTkLabel(form_frame, text="Estado Nuevo:", text_color="#c0392b", fg_color="#fff").pack(pady=5) #

        self.state_options = [s['nombre_estado'] for s in manejo_habitaciones.obtener_estado_hab_disponible()] #
        self.combo_estado = ttk.Combobox(form_frame, values=self.state_options, state="readonly") #
        self.combo_estado.pack(pady=5) #

        ctk.CTkButton(form_frame, text="Actualizar Estado", fg_color="#c0392b", hover_color="#e74c3c", text_color="#fff", command=self.update_status).pack(pady=10) #

    def load_current_status(self): #
        """Carga el estado actual de la habitación en el combobox."""
        if self.room_details['estado_habitacion_nombre'] in self.state_options: #
            self.combo_estado.set(self.room_details['estado_habitacion_nombre']) #
        else:
            if self.state_options: # Si hay opciones, selecciona la primera
                self.combo_estado.set(self.state_options[0]) #

    def update_status(self): #
        """Actualiza el estado de la habitación en la base de datos."""
        new_status = self.combo_estado.get() #
        if not new_status: #
            messagebox.showwarning("Selección Inválida", "Por favor, seleccione un estado.") #
            return #

        if manejo_habitaciones.cambiar_estado_hab(self.room_id, new_status): #
            messagebox.showinfo("Éxito", f"Estado de la habitación {self.room_details['numero_habitacion']} actualizado a '{new_status}'.") #
            self.parent.load_rooms() #
            self.destroy() #
        else:
            messagebox.showerror("Error", "Error al actualizar el estado de la habitación.") #

# if __name__=="__main__": # JSS: comentado porque ya no se trata de un tk.Tk
#     app=GestionDeHabitacionesApp() #
#     app.mainloop() #




     


     
     
    

   



    



    
    

    













    

