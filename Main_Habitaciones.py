
import tkinter as tk
from tkinter import  ttk, messagebox

import manejo_habitaciones #
import BD_Modulo_Habitaciones #

#Aplicación principal de gestión de habitaciones.
#Proporciona una interfaz gráfica para visualizar, añadir,
#editar y cambiar el estado de las habitaciones.
   
class GestionDeHabitacionesApp(ttk.Frame): #JSS: Se convirtió a frame para integrar a lo mío.
    def __init__(self, master): #JSS: ajustes de conversion a frame
        super().__init__(master, width=900, height=600) #JSS: ajustes de conversión a frame
        # self.title("Gestion de habitaciones") #JSS: comentado porque no se trata de un tk.Tk
        # self.geometry("900x600")  # Corregido: 90x600 era muy pequeño; JSS: comentado porque no se trata de un tk.Tk

        # Inicia la base de datos y el módulo de lógica de negocio
        # Así aseguramos que las tablas estén creadas al momento de iniciar la main app
        BD_Modulo_Habitaciones.crear_tablas() 
        manejo_habitaciones.iniciar_modulo_hab() #

        self.create_widgets() #
        self.load_rooms() #


    
    # Creación y organización de widgets para el usuario
    def create_widgets(self): #
        # Frame principal
        main_frame = ttk.Frame(self, padding="10") #
        main_frame.pack(fill=tk.BOTH, expand=True) #

        # Título
        ttk.Label(main_frame, text="Panel de gestión de habitaciones", font=("Arial", 16, "bold")).pack(pady=10) #

        # Tabla de habitación en Treeview
        self.room_tree = ttk.Treeview( #
            main_frame,
            columns=("ID", "Número", "Tipo", "Estado", "Ubicación", "Capacidad", "Notas"),
            show="headings"
        ) #
        self.room_tree.heading("ID", text="ID") #
        self.room_tree.heading("Número", text="Número") #
        self.room_tree.heading("Tipo", text="Tipo") #
        self.room_tree.heading("Estado", text="Estado") #
        self.room_tree.heading("Ubicación", text="Ubicación") #
        self.room_tree.heading("Capacidad", text="Capacidad") #
        self.room_tree.heading("Notas", text="Notas") #

        # Ancho de las columnas
        self.room_tree.column("ID", width=40, anchor=tk.CENTER) #
        self.room_tree.column("Número", width=80, anchor=tk.CENTER) #
        self.room_tree.column("Tipo", width=100, anchor=tk.W) #
        self.room_tree.column("Estado", width=100, anchor=tk.W) #
        self.room_tree.column("Ubicación", width=120, anchor=tk.W) #
        self.room_tree.column("Capacidad", width=70, anchor=tk.CENTER) #
        self.room_tree.column("Notas", width=200, anchor=tk.W) #

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.room_tree.yview) #
        self.room_tree.configure(yscrollcommand=scrollbar.set) #
        scrollbar.pack(side="right", fill="y") #

        self.room_tree.pack(fill=tk.BOTH, expand=True, pady=10) #

        # Botones de acción
        button_frame = ttk.Frame(main_frame) #
        button_frame.pack(pady=10) #

        ttk.Button(button_frame, text="Añadir habitación", command=self.open_add_room_window).pack(side=tk.LEFT, padx=5) #
        ttk.Button(button_frame, text="Editar habitación", command=self.open_edit_room_window).pack(side=tk.LEFT, padx=5) #
        ttk.Button(button_frame, text="Cambiar estado", command=self.open_change_status_window).pack(side=tk.LEFT, padx=5) #
        ttk.Button(button_frame, text="Eliminar habitación", command=self.delete_selected_room).pack(side=tk.LEFT, padx=5) # Corrected function call
        ttk.Button(button_frame, text="Actualizar Lista", command=self.load_rooms).pack(side=tk.LEFT, padx=5) #
        ttk.Button(button_frame, text="Atrás", command=self.master.atras_habitaciones).pack(side=tk.LEFT, padx=5)# JSS: agregada para volver a la pantalla principal

    def load_rooms(self): #
        """
        Carga todas las habitaciones desde la base de datos y las muestra en el Treeview.
        """
        for item in self.room_tree.get_children(): #
            self.room_tree.delete(item) #

        rooms = manejo_habitaciones.obtener_info_habitaciones() #
        for room in rooms: #
            self.room_tree.insert("", tk.END, iid=room['id_habitacion'], values=( #
                room['id_habitacion'], #
                room['numero_habitacion'], #
                room['tipo_habitacion'], #
                room['estado_habitacion'], #
                room['ubicacion'], #
                room['capacidad_maxima'], #
                room['notas_internas'] #
            ), tags=(room['estado_habitacion'].replace(" ", "_").lower(),)) # Tag para estilos si se desea

        # Aplicar estilos de color según el estado (ejemplo)
        self.room_tree.tag_configure("disponible", background="#e0ffe0") # Verde claro
        self.room_tree.tag_configure("ocupada", background="#ffe0e0")    # Rojo claro
        self.room_tree.tag_configure("sucia", background="#ffffd0")      # Amarillo claro
        self.room_tree.tag_configure("limpiando", background="#d0ffff")  # Azul cian claro
        self.room_tree.tag_configure("mantenimiento", background="#e0e0ff") # Púrpura claro
        self.room_tree.tag_configure("fuera_de_servicio", background="#cccccc") # Gris
    
    
    def open_add_room_window(self): #
        """
        Abre una nueva ventana para añadir una habitación.
        """
        AddRoomWindow(self) #

    def open_edit_room_window(self): #
        """
        Abre una nueva ventana para editar la habitación seleccionada.
        """
        selected_item = self.room_tree.focus() # Obtiene el ID del item seleccionado
        if not selected_item: #
            messagebox.showwarning("Editar Habitación", "Por favor, seleccione una habitación para editar.") #
            return #

        room_id = self.room_tree.item(selected_item, 'values')[0] # Obtiene el ID real de la habitación
        EditRoomWindow(self, room_id) #

    def open_change_status_window(self): #
        """
        Abre una nueva ventana para cambiar el estado de la habitación seleccionada.
        """
        selected_item = self.room_tree.focus() #
        if not selected_item: #
            messagebox.showwarning("Cambiar Estado", "Por favor, seleccione una habitación para cambiar su estado.") #
            return #

        room_id = self.room_tree.item(selected_item, 'values')[0] #
        ChangeStatusWindow(self, room_id) #

    def delete_selected_room(self): #
        """
        Elimina la habitación seleccionada de la base de datos.
        """
        selected_item = self.room_tree.focus() #
        if not selected_item: #
            messagebox.showwarning("Eliminar Habitación", "Por favor, seleccione una habitación para eliminar.") #
            return #

        room_id = self.room_tree.item(selected_item, 'values')[0] #
        room_number = self.room_tree.item(selected_item, 'values')[1] #

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro que desea eliminar la habitación {room_number} (ID: {room_id})?"): #
            if manejo_habitaciones.eliminar_habitacion(room_id): #
                messagebox.showinfo("Éxito", f"Habitación {room_number} eliminada exitosamente.") #
                self.load_rooms() #
            else:
                messagebox.showerror("Error", f"No se pudo eliminar la habitación {room_number}.") #


class AddRoomWindow(tk.Toplevel): #
    """
    Ventana para añadir una nueva habitación.
    """
    def __init__(self, parent): #
        super().__init__(parent) #
        self.title("Añadir Nueva Habitación") #
        self.geometry("350x300") #
        self.parent = parent #
        self.grab_set() # Hace que esta ventana sea modal

        self.create_form() #

    def create_form(self): #
        """Crea los campos del formulario para añadir una habitación."""
        form_frame = ttk.Frame(self, padding="10") #
        form_frame.pack(fill=tk.BOTH, expand=True) #

        ttk.Label(form_frame, text="Número de Habitación:").grid(row=0, column=0, padx=5, pady=5, sticky="w") #
        self.entry_numero = ttk.Entry(form_frame) #
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Tipo de Habitación:").grid(row=1, column=0, padx=5, pady=5, sticky="w") #
        self.type_options = [t['nombre_tipo'] for t in manejo_habitaciones.obtener_tipos_hab_disponible()] #
        self.combo_tipo = ttk.Combobox(form_frame, values=self.type_options, state="readonly") #
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="ew") #
        if self.type_options: #
            self.combo_tipo.set(self.type_options[0]) #

        ttk.Label(form_frame, text="Ubicación:").grid(row=2, column=0, padx=5, pady=5, sticky="w") #
        self.entry_ubicacion = ttk.Entry(form_frame) #
        self.entry_ubicacion.grid(row=2, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Capacidad Máxima:").grid(row=3, column=0, padx=5, pady=5, sticky="w") #
        self.entry_capacidad = ttk.Entry(form_frame) #
        self.entry_capacidad.grid(row=3, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Notas Internas:").grid(row=4, column=0, padx=5, pady=5, sticky="w") #
        self.entry_notas = ttk.Entry(form_frame) #
        self.entry_notas.grid(row=4, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Button(form_frame, text="Guardar", command=self.save_room).grid(row=5, column=0, columnspan=2, pady=10) #

        form_frame.columnconfigure(1, weight=1) # Permite que la columna de entradas se expanda

    def save_room(self): #
        """Guarda la nueva habitación en la base de datos."""
        numero = self.entry_numero.get().strip() #
        tipo = self.combo_tipo.get() #
        ubicacion = self.entry_ubicacion.get().strip() #
        capacidad_str = self.entry_capacidad.get().strip() #
        notas = self.entry_notas.get().strip() #

        if not numero or not tipo or not capacidad_str: #
            messagebox.showwarning("Entrada Inválida", "Número, Tipo y Capacidad son campos obligatorios.") #
            return #

        try: #
            capacidad = int(capacidad_str) #
            if capacidad <= 0: #
                raise ValueError #
        except ValueError: #
            messagebox.showwarning("Entrada Inválida", "Capacidad Máxima debe ser un número entero positivo.") #
            return #

        if manejo_habitaciones.agregar_nueva_hab(numero, tipo, ubicacion, capacidad, notas): #
            messagebox.showinfo("Éxito", f"Habitación {numero} añadida.") #
            self.parent.load_rooms() #
            self.destroy() #
        else:
            messagebox.showerror("Error", "Error al añadir habitación. Verifique si el número ya existe.") #


class EditRoomWindow(tk.Toplevel): #
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
        form_frame = ttk.Frame(self, padding="10") #
        form_frame.pack(fill=tk.BOTH, expand=True) #

        ttk.Label(form_frame, text="Número de Habitación:").grid(row=0, column=0, padx=5, pady=5, sticky="w") #
        self.entry_numero = ttk.Entry(form_frame) #
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Tipo de Habitación:").grid(row=1, column=0, padx=5, pady=5, sticky="w") #
        self.type_options = [t['nombre_tipo'] for t in manejo_habitaciones.obtener_tipos_hab_disponible()] #
        self.combo_tipo = ttk.Combobox(form_frame, values=self.type_options, state="readonly") #
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Estado Actual:").grid(row=2, column=0, padx=5, pady=5, sticky="w") #
        self.state_options = [s['nombre_estado'] for s in manejo_habitaciones.obtener_estado_hab_disponible()] #
        self.combo_estado = ttk.Combobox(form_frame, values=self.state_options, state="readonly") #
        self.combo_estado.grid(row=2, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Ubicación:").grid(row=3, column=0, padx=5, pady=5, sticky="w") #
        self.entry_ubicacion = ttk.Entry(form_frame) #
        self.entry_ubicacion.grid(row=3, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Capacidad Máxima:").grid(row=4, column=0, padx=5, pady=5, sticky="w") #
        self.entry_capacidad = ttk.Entry(form_frame) #
        self.entry_capacidad.grid(row=4, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Label(form_frame, text="Notas Internas:").grid(row=5, column=0, padx=5, pady=5, sticky="w") #
        self.entry_notas = ttk.Entry(form_frame) #
        self.entry_notas.grid(row=5, column=1, padx=5, pady=5, sticky="ew") #

        ttk.Button(form_frame, text="Guardar Cambios", command=self.save_changes).grid(row=6, column=0, columnspan=2, pady=10) #
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


class ChangeStatusWindow(tk.Toplevel): #
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
        form_frame = ttk.Frame(self, padding="10") #
        form_frame.pack(fill=tk.BOTH, expand=True) #

        ttk.Label(form_frame, text=f"Habitación: {self.room_details['numero_habitacion']}").pack(pady=5) #
        ttk.Label(form_frame, text="Estado Nuevo:").pack(pady=5) #

        self.state_options = [s['nombre_estado'] for s in manejo_habitaciones.obtener_estado_hab_disponible()] #
        self.combo_estado = ttk.Combobox(form_frame, values=self.state_options, state="readonly") #
        self.combo_estado.pack(pady=5) #

        ttk.Button(form_frame, text="Actualizar Estado", command=self.update_status).pack(pady=10) #

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




     


     
     
    

   



    



    
    

    













    

