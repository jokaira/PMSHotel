#importacion de librerias para la interfaz gráfica y base de datos
import customtkinter as ctk
import sqlite3 as sql #para conexión y queries a la base de datos
import tkinter as tk
from tkinter import ttk, messagebox #widgets mas modernos y cuadros de dialogo

class GestorClientes(ctk.CTkFrame):
    #modulo completo de gestión de clientes
    def __init__(self, master):
        super().__init__(master)
        
        #frame principal
        self.configure(fg_color = "transparent")

        #inicializacion de variables de control
        self.cliente_actual = None #almacena el cliente seleccionado
        self.busqueda_var = tk.StringVar() #campo de busqueda

        #creacion de interfaz de usuario
        self.setup_ui() #configura la interfaz

        #cargar datos
        self.cargar_clientes() #carga la lista de clientes
    
    def setup_ui(self):
        #configura la interfaz de usuario
        #crea todos los elementos visuales como encabezadp, área de búsqueda, tabla y botones.

        #frame principal del modulo
        main_frame = ctk.CTkFrame(self, fg_color = "#fff", corner_radius = 15)
        main_frame.pack(fill = "both", expand = True, padx = 20, pady = 20)

        #encabezado del modulo
        self.create_header(main_frame)

        #área de búsqueda y filtros
        self.create_search_area(main_frame)

        #tabla de clientes
        self.create_table(main_frame)

        #area de botones
        self.create_action_buttons(main_frame)

    def create_header(self, parent):
        #crea el encabezado del modulo con titulo y boton de regreso

        #frame del encabezado
        header_frame = ctk.CTkFrame(parent, fg_color = "#c0392b", corner_radius=10, height=60)
        header_frame.pack(fill = "x", padx = 20, pady = (20, 10))
        header_frame.pack_propagate(False)

        #boton de regreso
        back_btn = ctk.CTkButton(header_frame, text="← Volver", fg_color="transparent", text_color="white", font=("Arial", 12, "bold"), hover_color="#e74c3c", command=self.go_back)
        back_btn.pack(side="left", padx = 20, pady = 15)

        #titulo del modulo
        title_label = ctk.CTkLabel(header_frame, text = "👥 Gestión de Clientes", font=("Arial", 20, "bold"), text_color="white")
        title_label.pack(side="left", padx=(20, 0), pady=(15))

    def create_search_area(self, parent):
        #crea el area de busqueda y filtros

        #frame del area de busqueda
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill = "x", padx = 20, pady = 10)

        #label del campo de busqueda
        search_label = ctk.CTkLabel(search_frame, text="🔍 Buscar Cliente:", font=("Arial", 12, "bold"), text_color="#2c3e50")
        search_label.pack(side = "left", padx = (0, 10))

        #campo de busqueda
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.busqueda_var, placeholder_text="Ingrese nombre, email o teléfono...", width = 300, height=35, font=("Arial", 12), border_color="#c0392b", fg_color="#f8f9fa")
        self.search_entry.pack(side="left", padx = (0, 10))

        #boton de busqueda
        search_btn = ctk.CTkButton(search_frame, text="Buscar", fg_color="#c0392b", text_color="white", font=("Arial", 12, "bold"), width=100, height = 35, hover_color="#e74c3c", command = self.buscar_cliente)
        search_btn.pack(side="left", padx=(0, 10))

        #boton para limpiar busqueda
        clear_btn = ctk.CTkButton(search_frame, text="Limpiar", fg_color="#95a5a6", text_color="white", font=("Arial", 12, "bold"), width = 100, height = 35, hover_color= "#7f8c8d", command=self.limpiar_busqueda)
        clear_btn.pack(side="left")

    def create_table(self, parent):
        #crea la tabla de clientes

        #frame para la tabla
        table_frame = ctk.CTkFrame(parent, fg_color = "transparent")
        table_frame.pack(fill = "both", expand = True, padx = 20, pady = 20)

        #tabla (treeview)
        columns = ("Nombres", "Apellidos", "Documento", "Nro. Doc", "Cumpleaños", "Género", "Nacionalidad", "Teléfono", "E-mail")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height = 2)

        #bucle para configurar columnas de la tabla
        i = 0 #variable pal bucle
        for column in columns:
            i += 1
            if i == len(column):
                self.tree.column(column=f"# {i}", anchor=tk.CENTER, width=190) #esto es para la columna del email, ya que no cabe en 100 y justamente es el ultimo elemento del bucle
            else:
                self.tree.column(column=f"# {i}", anchor=tk.CENTER, width=100)
            self.tree.heading(column=f"# {i}", text=column)

        # scrollbars para la tabla 
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command= self.tree.yview)#scroll vertical
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command= self.tree.xview)#scroll horizontal

        #conexion de los scrollbars a la tabla
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        #pack de la tabla y scrolls
        self.tree.grid(row = 0, column= 0, sticky= "nsew") #indica que debe expandirse y alinearse en todas las direcciones posibles, n = norte, s = sur, e = este, w = oeste
        vsb.grid(row=0, column=1, sticky="ns")#solo se expande y se alinea norte a sur
        hsb.grid(row=1, column=0, sticky="ew")#solo se expande y se alinea este a oeste

        #configuracion del grid para que se expanda
        table_frame.grid_rowconfigure(0, weight=1) #configura la fila 0 para que se expanda
        table_frame.grid_columnconfigure(0, weight=1)#configura la columna 0 para que se expanda

        #seleccion de fila
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_action_buttons(self, parent):
        #crea los botones para gestionar los clientes

        #frame para botones
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill = "x", padx = 20, pady = 20)

        #estilo para todos los botones
        button_style = {
            "font": ("Arial", 12, "bold"),
            "height": 40,
            "corner_radius": 10,
            "width": 120
        }

        #boton para agregar nuevo cliente
        add_btn = ctk.CTkButton(button_frame, text="➕ Agregar", fg_color="#27ae60", text_color="white", hover_color="#2ecc71", command=self.agregar_cliente, **button_style)
        add_btn.pack(side="left", padx=(0, 10))

        #boton para editar cliente
        edit_btn = ctk.CTkButton(button_frame, text="✏️ Editar", fg_color="#f39c12", text_color="white", hover_color="#e67e22", command=self.editar_cliente, **button_style)
        edit_btn.pack(side = "left", padx=(0, 10))

        #boton para eliminar cliente
        delete_btn = ctk.CTkButton(button_frame, text="🗑️ Eliminar", fg_color="#e74c3c", text_color="white", hover_color="#c0392b", command=self.eliminar_cliente, **button_style)
        delete_btn.pack(side="left", padx=(0, 10))

        #boton para refrescar lista
        refresh_btn = ctk.CTkButton(button_frame, text="🔄 Refrescar", fg_color="#3498db", text_color="white", hover_color="#2980b9", command=self.cargar_clientes, **button_style)
        refresh_btn.pack(side="left")

    def go_back(self):
        #metodo para regresar al dashboard principal
        parent = self.master #obtiene el widget padre
        while parent:
            if hasattr(parent, "atras_clientes"): #verifica que el padre tenga este metodo
                parent.atras_clientes()
                break
            parent=parent.master #obtiene el siguiente widget padre

    def cargar_clientes(self):
        # carga la lista de clientes y los muestra en la tabla

        #limpia la tabla antes de cargar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sql.connect("base_datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email FROM cliente ORDER BY nombres")
            clientes = cursor.fetchall()

            #inserta clientes en tabla
            for cliente in clientes:
                self.tree.insert("", "end", values=cliente)

            conn.close()
        except sql.Error as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {e}")

    def buscar_cliente(self):
        #busca clientes por nombres, apellidos, nro. doc, telefono e email

        #obtiene el texto de búsqueda
        busqueda = self.busqueda_var.get().strip()  #obtiene y limpia el texto
        
        if not busqueda:
            self.cargar_clientes()
            return
        
        #limpia la tabla antes de mostrar resultados
        for item in self.tree.get_children():  #itera sobre todos los elementos
            self.tree.delete(item)
        
        try:
            #establece conexión con la base de datos
            conn = sql.connect('base_datos.db')
            cursor = conn.cursor()
            
            #ejecuta consulta de búsqueda con parámetros
            cursor.execute("""
                SELECT * FROM cliente 
                WHERE nombres LIKE ? OR apellidos LIKE ? OR email LIKE ? OR telefono LIKE ? OR numero_doc LIKE ?
                ORDER BY nombres
            """, (f'%{busqueda}%', f'%{busqueda}%', f'%{busqueda}%', f'%{busqueda}%', f'%{busqueda}%'))
            clientes = cursor.fetchall()

            #inserta los resultados en la tabla
            for cliente in clientes:
                self.tree.insert("", "end", values=cliente)
            conn.close()
        except sql.Error as e:
            # Muestra mensaje de error
            messagebox.showerror("Error", f"Error al buscar clientes: {e}")

    def limpiar_busqueda(self):
        # limpia el campo de busqueda y recarga todos los clientes
        self.busqueda_var.set("")
        self.cargar_clientes()

    def on_select(self):
        #evento de seleccion de una fila en la tabla, almacena la info del cliente seleccionado

        #obtiene la fila seleccionada
        selection = self.tree.selection()

        if selection:
            item = self.tree.item(selection[0])
            self.cliente_actual = item["values"]

    def agregar_cliente(self):
        #abre la ventana de dialogo para agrega un nuevo cliente

        #creacion de la ventana de dialogo
        dialog = ctk.CTkToplevel(self)
        dialog.title("Agregar Nuevo Cliente")
        dialog.geometry("500x400")
        dialog.resizable(False, False) #para que se quede con tamaño constante
        dialog.transient(self) #se mantiene siempre delante de la principal, y se cierra si la principal se cierra
        dialog.grab_set() #hace que no se pueda usar la ventana principal hasta que se cierre o complete la ventana de dialogo

        #frame principal del dialogo
        main_frame = ctk.CTkFrame(dialog, fg_color = "#fff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        #titulo
        title_label = ctk.CTkLabel(main_frame, text = "➕ Agregar Nuevo Cliente", font = ("Arial", 18, "bold"), text_color="#2c3e50")
        title_label.pack(pady=(0, 20))

        #campos del formulario
        self.create_form_fields(main_frame, dialog, "agregar") #metodo para crear campos

    def editar_cliente(self):
        #abre la ventana de dialogo para editar un cliente seleccionado

        #verifica que haya un cliente seleccionado
        if not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente para editar")
            return
        
        #creacion de la ventana de dialogo
        dialog = ctk.CTkToplevel(self)
        dialog.title("Editar Cliente")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        #frame principal
        main_frame = ctk.CTkFrame(dialog, fg_color = "#fff")
        main_frame.pack(fill="both", expand = True, padx = 20, pady = 20)

        #titulo
        title_label = ctk.CTkLabel(main_frame, text="✏️ Editar Cliente", font=("Arial", 18, "bold"), text_color="#2c3e50")
        title_label.pack(pady = (0, 20))

        #creacion de campos del formulario
        self.create_form_fields(main_frame, dialog, "editar")
 
    def eliminar_cliente(self):
        # elimina el cliente seleccionado de la base de datos

        if not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente para eliminar")
            return
        
        #confirmacion antes de eliminar
        confirmacion = messagebox.askyesno("Confirmar eliminacion", f"¿Está seguro que desea eliminar al cliente: \n{self.cliente_actual[1]}?")

        if confirmacion:
            try:
                conn = sql.connect("base_datos.db")
                cursor = conn.cursor()

                cursor.execute("DELETE FROM cliente WHERE numero_doc = ?", (self.cliente_actual[3],))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")

                self.cargar_clientes()
                self.cliente_actual = None
            except sql.Error as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {e}")

    def create_form_fields(self, parent, dialog, mode):
        #crea los campos del formulario pa agregar y editar clientes
        #argumentos:
            #parent: widget padre
            #dialog: ventana de dialogo
            #mode: modo del formulario (agregar o editar)
        
        #frame para los campos
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)

        #variables de los campos
        nombres_var = tk.StringVar()
        apellidos_var = tk.StringVar()
        tipo_doc_var = tk.StringVar()
        numero_doc_var = tk.StringVar()
        fecha_nac_var = tk.StringVar()
        genero_var = tk.StringVar()
        nacionalidad_var = tk.StringVar()
        telefono_var = tk.StringVar()
        email_var = tk.StringVar()

        #modo editar
        if mode == "editar" and self.cliente_actual:
            nombres_var.set(self.cliente_actual[0])
            apellidos_var.set(self.cliente_actual[1])
            tipo_doc_var.set(self.cliente_actual[2])
            numero_doc_var.set(self.cliente_actual[3])
            fecha_nac_var.set(self.cliente_actual[4])
            genero_var.set(self.cliente_actual[5])
            nacionalidad_var.set(self.cliente_actual[6])
            telefono_var.set(self.cliente_actual[7])
            email_var.set(self.cliente_actual[8])

        #campo de nombres
        nombres_label = ctk.CTkLabel(form_frame, text="Nombres:", font=("Arial", 12, "bold"))
        nombres_label.pack(anchor="w", pady=(0, 5))
        
        nombres_entry = ctk.CTkEntry(form_frame, textvariable=nombres_var, placeholder_text="Ingrese los nombres", height=35, font=("Arial", 12))
        nombres_entry.pack(fill="x", pady=(0, 15))

        #campo de apellidos
        apellidos_label = ctk.CTkLabel(form_frame, text="Apellidos:", font=("Arial", 12, "bold"))
        apellidos_label.pack(anchor="w", pady=(0, 5))

        apellidos_entry = ctk.CTkEntry(form_frame, textvariable=apellidos_var, placeholder_text="Ingrese los apellidos", height=35, font=("Arial", 12))
        apellidos_entry.pack(fill="x", pady=(0, 15))

        #combobox de tipo de documento
        tipo_doc_label = ctk.CTkLabel(form_frame, text="Tipo de Documento:", font=("Arial", 12, "bold"))
        tipo_doc_label.pack(anchor="w", pady=(0, 5))

        tipo_doc_combobox = ttk.Combobox(form_frame, textvariable=tipo_doc_var, values=["Cédula", "Pasaporte"], state="readonly",  font=("Arial", 12), height=35)
        tipo_doc_combobox.pack(fill="x", pady=(0, 15))

        #campo de numero de documento
        numero_doc_label = ctk.CTkLabel(form_frame, text="Número de Documento:", font=("Arial", 12, "bold"))
        numero_doc_label.pack(anchor="w", pady=(0, 5))

        numero_doc_entry = ctk.CTkEntry(form_frame,textvariable=numero_doc_var, placeholder_text="Ingrese el número de documento", height=35, font=("Arial", 12))
        numero_doc_entry.pack(fill="x", pady=(0, 20))

        #campo de cumpleaños
        fecha_nac_label = ctk.CTkLabel(form_frame, text="Cumpleaños", font=("Arial", 12, "bold"))
        fecha_nac_label.pack(anchor="w", pady=(0, 5))

        fecha_nac_entry = ctk.CTkEntry(form_frame, textvariable=fecha_nac_var, placeholder_text="Ingrese la fecha de nacimiento", height=35, font=("Arial", 12))
        fecha_nac_entry.pack(fill="x", pady=(0, 15))

        #campo de genero
        genero_label = ctk.CTkLabel(form_frame, text="Cumpleaños", font=("Arial", 12, "bold"))
        genero_label.pack(anchor="w", pady=(0, 5))

        genero_entry = ctk.CTkEntry(form_frame, textvariable=genero_var, placeholder_text="Ingrese el genero", height=35, font=("Arial", 12))
        genero_entry.pack(fill="x", pady=(0, 15))

        #campo de nacionalidad
        nacionalidad_label = ctk.CTkLabel(form_frame, text="Cumpleaños", font=("Arial", 12, "bold"))
        nacionalidad_label.pack(anchor="w", pady=(0, 5))

        nacionalidad_entry = ctk.CTkEntry(form_frame, textvariable=nacionalidad_var, placeholder_text="Ingrese la nacionalidad", height=35, font=("Arial", 12))
        nacionalidad_entry.pack(fill="x", pady=(0, 15))

        #campo de telefono
        telefono_label = ctk.CTkLabel(form_frame, text="Teléfono:", font=("Arial", 12, "bold"))
        telefono_label.pack(anchor="w", pady=(0, 5))

        telefono_entry = ctk.CTkEntry(form_frame, textvariable=telefono_var, placeholder_text="Ingrese el teléfono", height=35, font=("Arial", 12))
        telefono_entry.pack(fill="x", pady=(0, 15))

        #campo de email
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 12, "bold"))
        email_label.pack(anchor="w", pady=(0, 5))

        email_entry = ctk.CTkEntry(form_frame, textvariable=email_var, placeholder_text="Ingrese el email", height=35, font=("Arial", 12) )
        email_entry.pack(fill="x", pady=(0, 15))  # Empaqueta horizontalmente con padding

        #frame para los botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        def guardar():
            #funcion para guardar datos del formulario
            nombres = nombres_var.get().strip()
            apellidos = apellidos_var.get().strip()
            tipo_doc = tipo_doc_var.get()
            numero_doc = numero_doc_var.get().strip()
            fecha_nac = fecha_nac_var.get().strip()
            genero = genero_var.get().strip()
            nacionalidad = nacionalidad_var.get().strip()
            telefono = telefono_var.get().strip()
            email = email_var.get().strip()

            #validacion de campos obligatorios
            if not nombres or not email or not telefono or not numero_doc:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            try:
                conn = sql.connect("base_datos.db")
                cursor=conn.cursor()

                if mode == "agregar": #si es para agregar cliente
                    cursor.execute("""
                    INSERT INTO cliente (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email))
                    messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                else: #si es editar cliente
                    cursor.execute("""
                    UPDATE cliente 
                    SET nombres = ?, apellidos = ?, tipo_doc = ?, numero_doc = ?, fecha_nac = ?, genero = ?, nacionalidad = ?, telefono = ?, email = ?
                    WHERE numero_doc = ?
                    """, (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email, self.cliente_actual[3]))
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                
                conn.commit()
                conn.close()
                dialog.destroy()
                self.cargar_clientes()

            except sql.Error as e:
                messagebox.showerror("Error", f"Error al guardar cliente: {e}")

        #boton de guardar
        guardar_btn = ctk.CTkButton(button_frame, text="💾 Guardar", fg_color="#27ae60", text_color="white", font=("Arial", 12, "bold"), height=35, command=guardar)
        guardar_btn.pack(side="left", padx=(0, 10))

        #boton de cancelar
        cancelar_btn = ctk.CTkButton(button_frame, text="❌ Cancelar", fg_color = "#95a5a6", text_color="white", font=("Arial", 12, "bold"), height=35, command=dialog.destroy)
        cancelar_btn.pack(side="left")
        





#para probar sin tener que entrar al main, hay que comentarlo cuando se usa desde el main porque si no, no abre  
# root = tk.Tk()
# root.geometry(f"{res_ventana['x']}x{res_ventana['y']}")
# root.resizable(False, False)
# GestorClientes(root).place(relx=0.5, rely=0.5, anchor="center")
# root.mainloop()