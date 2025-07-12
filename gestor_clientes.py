# WARNING: ESTA VAINA ES PRACTICAMENTE UN CRUD, PERO EL PROGRAMITA ESE ESTÁ PEOR QUE LO QUE COLOQUÉ AQUÍ

import sqlite3 as sql #para conexión y queries a la base de datos
import tkinter as tk #interfaz
from tkinter import ttk #widgets mas modernos y la tabla esa
from tkinter import messagebox #para mensajes de error

res_ventana = {"x": 1024, "y": 768} #la resolución de la ventana

class GestorClientes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, width=res_ventana["x"]*0.97, height=res_ventana["y"]*0.97)
        
        #el título del módulo de gestión de clientes
        self.titulo = ttk.Label(master=self, text="Gestor de Clientes", font=("Arial", 20, "bold"))
        self.titulo.place(relx=0.5, rely=0.04, anchor="center")

        #botón pa volver atrás
        self.atras_btn = ttk.Button(self, text="Atrás", command=self.master.atras_clientes) 
        #la función atrás_clientes está en el main, y hay que comentar el jodio boton este si no se corre del main porque si no, no abre
        self.atras_btn.place(relx=0.85, rely=0.9)

        #el estila para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="white", background="firebrick3",borderwidth=0)

        #los encabezados de las columnas
        self.columnas = ("Nombres", "Apellidos", "Documento", "Nro. Doc", "Cumpleaños", "Género", "Nacionalidad", "Teléfono", "E-mail")

        #esto genera la tabla
        self.tree = ttk.Treeview(self,columns=self.columnas, show='headings', height=20)
        self.i = 0 #esta variable es para el bucle for para agregar las columnas

        #el bucle for para agregar las columnas
        for columna in self.columnas:
            self.i += 1
            if self.i == len(self.columnas):
                self.tree.column(column=f"# {self.i}", anchor=tk.CENTER, width=190) #esto es para la columna del email, ya que no cabe en 100 y justamente es el ultimo elemento del bucle
            else:
                self.tree.column(column=f"# {self.i}", anchor=tk.CENTER, width=100)
            self.tree.heading(column=f"# {self.i}", text=columna)

        #este bucle inserta las filas desde la base de datos
        for row in self.mostrar_clientes():
            self.tree.insert("", "end", values=[str(item) for item in row])
        self.tree.place(relx=0.5, rely=0.5, anchor="center")

        #botones para agregar, modificar y eliminar clientes
        self.agregar_btn = ttk.Button(self, text="Agregar", command=self.agregar_cliente)
        self.agregar_btn.place(relx=0.15, rely=0.9)

        self.modificar_btn = ttk.Button(self, text="Modificar", command=self.modificar_cliente)
        self.modificar_btn.place(relx=0.325, rely=0.9)

        self.eliminar_btn = ttk.Button(self, text="Eliminar", command=self.eliminar_cliente)
        self.eliminar_btn.place(relx=0.50, rely=0.9)

    def actualizar_treeview(self): #esto es pa actualizar los datos de la tabla
        try:
            #borrar todos los elementos del treeview
            self.tree.delete(*self.tree.get_children())

            #obtener e insertar nuevos datos a mostrar
            for row in self.mostrar_clientes():
                self.tree.insert("", "end", values=[str(item) for item in row])
        except ValueError as error:
            print("Error al actualizar tabla: ", error)

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