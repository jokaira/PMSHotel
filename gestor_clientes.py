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
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height = 15)

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

    #aqui ta la función pa agregar un cliente 
    def agregar_cliente(self):
        #ventanita de agregar y editar la info de los clientes
        ventanita = tk.Toplevel(master=self.master)
        ventanita.title("Agregar cliente")
        ventanita.geometry("300x500")
        
        captura_entry = [] #esto es pa almacenar los datos de los entry que fueron generados en el bucle for 
        i = 0
        for campo in self.columnas: #esto me genera un label y un campo sin tener que hacerlo manualmente
            i += 1
            ttk.Label(ventanita, text=campo).pack(pady=3)
            valor_entry = tk.StringVar()
            if i == 3: #esto es pa agregar una lista desplegable donde va el tipo de documento
                ttk.Combobox(master=ventanita, values=["Cédula", "Pasaporte"], textvariable=valor_entry).pack()
            else:
                ttk.Entry(ventanita, textvariable=valor_entry).pack()
            captura_entry.append(valor_entry)
        
        def guardar_cliente():
            datos_entry = [var.get() for var in captura_entry] #convierte los datos del entry en strings
            try:
                conexion = sql.connect("base_datos.db")
                conexion.autocommit = True
                cursor = conexion.cursor()
                cursor.execute("""INSERT INTO cliente (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email) VALUES (?,?,?,?,?,?,?,?,?)""", datos_entry)
                print(cursor.rowcount, "Registro insertado")
                conexion.close()
                messagebox.showinfo("Información", "Los datos fueron guardados exitosamente")
                ventanita.destroy()
                self.actualizar_treeview()
            except sql.Error as error:
                messagebox.showerror("Error", f"Ha ocurrido un error al guardar los datos: {error}")
         

        guardar_btn = ttk.Button(ventanita, text="Guardar", command=guardar_cliente)
        guardar_btn.pack(pady=10)

    #aqui ta la funcion pa modificar un cliente
    def modificar_cliente(self):
        id_seleccion = self.tree.selection()
        if not id_seleccion:
            messagebox.showerror("Error", "No se ha seleccionado ningun cliente para modificar")
            return
        seleccion = self.tree.item(id_seleccion[0], "values")

        # ventanita de agregar y editar la info de los clientes
        ventanita = tk.Toplevel(master=self.master)
        ventanita.title("Modificar cliente")
        ventanita.geometry("300x500")
        
        captura_entry = [] #esto es pa almacenar los datos de los entry que fueron generados en el bucle for 

        i = 0
        for campo in self.columnas: #esto me genera un label y un campo sin tener que hacerlo manualmente
            i += 1
            ttk.Label(ventanita, text=campo).pack(pady=3)
            if i == 3: #esto es pa agregar una lista desplegable donde va el tipo de documento
                combobox = ttk.Combobox(master=ventanita, values=["Cédula", "Pasaporte"])
                combobox.pack()
                combobox.set(seleccion[i-1])
                captura_entry.append(combobox)
            else:
                entry = ttk.Entry(ventanita)
                entry.pack()
                entry.insert(0, seleccion[i-1])
                captura_entry.append(entry)
            
        def modificar_cliente():
            datos_entry = [var.get() for var in captura_entry] #convierte los datos del entry en strings
            try:
                conexion = sql.connect("base_datos.db")
                conexion.autocommit = True
                cursor = conexion.cursor()
                cursor.execute("""UPDATE cliente SET nombres = ?, apellidos = ?, tipo_doc = ?, numero_doc = ?, fecha_nac = ?, genero = ?, nacionalidad = ?, telefono = ?, email = ? WHERE numero_doc = ?""", (*datos_entry, seleccion[3]))
                print(cursor.rowcount, "Registro modificado")
                conexion.close()
                messagebox.showinfo("Información", "Los datos fueron modificados exitosamente")
                ventanita.destroy()
                self.actualizar_treeview()
            except sql.Error as error:
                messagebox.showerror("Error", f"Ha ocurrido un error al modificar los datos: {error}")
        
        modificar_btn = ttk.Button(ventanita, text="Modificar", command=modificar_cliente)
        modificar_btn.pack(pady=10)
 
    #aqui ta la función pa eliminar un cliente
    def eliminar_cliente(self):
        id_seleccion = self.tree.selection()
        if not id_seleccion:
            messagebox.showerror("Error", "No se ha seleccionado ningun cliente para eliminar")
            return
        seleccion = self.tree.item(id_seleccion[0], "values")

        respuesta = messagebox.askyesnocancel("Advertencia", "¿Está seguro que desea eliminar los datos de este cliente?")
        if respuesta is True:
            try:
                conexion = sql.connect("base_datos.db")
                conexion.autocommit = True
                cursor = conexion.cursor()
                cursor.execute(f"""DELETE FROM cliente WHERE numero_doc = ?""", (seleccion[3],))
                print(cursor.rowcount, "Registro eliminado")
                conexion.close()
                messagebox.showinfo("Información", "Los datos fueron eliminados exitosamente")
                self.actualizar_treeview()
            except sql.Error as error:
                messagebox.showerror("Error", f"Ha ocurrido un error al eliminar los datos: {error}")
        else:
            pass

    #esta es la función que llena la tabla en el programa desde la base de datos
    def mostrar_clientes(self):
        try:
            conexion = sql.connect("base_datos.db")
            conexion.autocommit = True
            cursor = conexion.cursor()
            cursor.execute("""select nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email
            from cliente""")
            resultado = cursor.fetchall()
            conexion.close()
            return resultado
        except sql.Error as error:
            messagebox.showerror("Error", f"Ha ocurrido un error al consultar la base de datos: {error}")






#para probar sin tener que entrar al main, hay que comentarlo cuando se usa desde el main porque si no, no abre  
# root = tk.Tk()
# root.geometry(f"{res_ventana['x']}x{res_ventana['y']}")
# root.resizable(False, False)
# GestorClientes(root).place(relx=0.5, rely=0.5, anchor="center")
# root.mainloop()