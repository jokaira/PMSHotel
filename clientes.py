import customtkinter as ctk
from settings import *
from func_clases import *
from tkinter import messagebox
from datetime import datetime
from email_validator import validate_email, EmailNotValidError #para validar correo electronico

class GestorClientes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #data
        self.cliente_actual = None
        self.busqueda_var = ctk.StringVar()

        #barra de busqueda + botones
        self.barra = self.barra_buscar()

        #contenedor de la tabla de clientes
        self.contenedor_tabla = ctk.CTkFrame(self, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = 12)

        #tabla de clientes
        self.tabla_clientes(data=[ENCABEZADOS_CLIENTES] + [c for c in CLIENTES()])

        #botones acción
        self.botones = self.crear_botones()

    def barra_buscar(self):
        contenedor = ctk.CTkFrame(self, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=62)
        contenedor.pack(fill = 'x')
        contenedor.pack_propagate(False)

        ctk.CTkLabel(contenedor, 
                     text='🔍 Buscar:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkEntry(contenedor,
                     placeholder_text='Nombre, email o teléfono...',
                     placeholder_text_color=GRIS_CLARO2,
                     corner_radius=8,
                     text_color=OSCURO,
                     textvariable=self.busqueda_var,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35
                     ).pack(side = 'left', fill = 'x', expand = True, padx = 6)
        
        btn_buscar = Boton(master=contenedor,
                           texto = 'Buscar', 
                           fill=None, 
                           padx=(12,6),
                           metodo=self.buscar_cliente
                           )

        btn_limpiar = Boton(master=contenedor,
                            texto='Limpiar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None,
                            metodo=self.limpiar_busqueda
                            )

        btn_agregar = Boton(master=contenedor,
                            texto='➕ Agregar',
                            color=VERDE1,
                            hover=VERDE2,
                            fill=None,
                            padx=(6,12),
                            metodo = lambda: self.modal_cliente("agregar")
                            )

    def tabla_clientes(self, data): 
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

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
                
                  lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                  lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)
                  
                  frame.grid_columnconfigure(c, weight=1)

                  #borde encabezado
                  if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column = c, sticky = 'ew')
                    borde.grid_propagate(False)
                    borde.configure(height = 2)

                  #bind capturando fila
                  if f > 0:
                    lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion(fila))
                  fila_widgets.append(lbl)
            self.celdas.append(fila_widgets)

    def buscar_cliente(self):
            busqueda = self.busqueda_var.get().strip()

            if not busqueda:
                self.tabla_clientes([ENCABEZADOS_CLIENTES] + [c for c in CLIENTES()])
                return
            
            #buscar clientes
            resultado = basedatos.buscar_cliente(busqueda)
            data = [ENCABEZADOS_CLIENTES] + resultado
            self.tabla_clientes(data=data)

    def limpiar_busqueda(self):
         self.busqueda_var.set('')
         self.tabla_clientes(data=[ENCABEZADOS_CLIENTES] + [c for c in CLIENTES()])

    def crear_botones(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=10, border_color=GRIS_CLARO3, border_width=1)
        btn_frame.pack(anchor = 'n', fill = 'x', expand = True, padx = 12, pady = 12)

        self.btn_editar = Boton(master=btn_frame,
                           texto='Editar',
                           color=MAMEY,
                           hover=MAMEY2,
                           tamano_texto=12,
                           altura=28,
                           fill=None,
                           metodo= lambda: self.modal_cliente("editar")
                           )

        self.btn_eliminar = Boton(master=btn_frame,
                           texto='Eliminar',
                           color=ROJO,
                           hover=ROJO2,
                           tamano_texto=12,
                           altura=28,
                           fill=None,
                           metodo= self.eliminar_cliente
                           )
        
    def seleccion(self, fila):
        if fila == 0:
             return
        valores = [w.cget('text') for w in self.celdas[fila]]
        self.cliente_actual = valores
        print(self.cliente_actual)

        #resaltado
        for f, fila_widgets in enumerate(self.celdas):
             for w in fila_widgets:
                w.configure(fg_color = AZUL_CLARO if f == fila else ('transparent' if f%2 == 0 else GRIS_CLARO4))

    def validar_email(self, email):
        if not email:
            return False, "El correo electrónico es obligatorio"
        try:
            valido = validate_email(email)
            email_normalizado = valido.email
            return True, "Email válido"
        except EmailNotValidError as e:
            return False, f"El formato del correo electrónico no es válido: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado al validar email: {str(e)}"
    
    def modal_cliente(self, tipo):
        if tipo == "editar" and not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente para editar")
            return

        dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
        dialogo.title("Agregar Nuevo Cliente" if tipo == "agregar" else "Editar Cliente")
        dialogo.geometry("720x380")
        dialogo.resizable(False,False)
        dialogo.transient(self)
        dialogo.grab_set()
        
        #titulo
        ctk.CTkLabel(dialogo, 
                     text= "➕ Nuevo Cliente" if tipo == "agregar" else "✏️ Editar Cliente", 
                     text_color=OSCURO, 
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', pady = (16,0), padx = 16)
        
        ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

        self.crear_formulario(master=dialogo, tipo= tipo)
        
    def eliminar_cliente(self):
        if not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente para eliminar")
            return
        
        confirmacion = messagebox.askyesno("Eliminar cliente", f"¿Está seguro que desea eliminar a este cliente?\n{self.cliente_actual[1]} {self.cliente_actual[2]}")

        if confirmacion:
            try:
              eliminacion = basedatos.eliminar_cliente(self.cliente_actual[0])
              messagebox.showinfo("Éxito", eliminacion[1])
            except:
              messagebox.showerror("Error", eliminacion[1])

        #actualizar tabla
        from settings import CLIENTES
        self.tabla_clientes(data=[ENCABEZADOS_CLIENTES] + [c for c in CLIENTES()])

    def crear_formulario(self, master, tipo):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        #variables de los campos
        nombres = ctk.StringVar()
        apellidos = ctk.StringVar()
        tipo_doc = ctk.StringVar(value='Cédula')
        numero_doc = ctk.StringVar()
        fecha_nac = ctk.StringVar()
        genero = ctk.StringVar()
        nacionalidad = ctk.StringVar()
        telefono = ctk.StringVar()
        email = ctk.StringVar()
        
        #modo editar
        if tipo == "editar":
            nombres.set(self.cliente_actual[1])
            apellidos.set(self.cliente_actual[2])
            tipo_doc.set(self.cliente_actual[3])
            numero_doc.set(self.cliente_actual[4])
            fecha_nac.set(self.cliente_actual[5])
            genero.set(self.cliente_actual[6])
            nacionalidad.set(self.cliente_actual[7])
            telefono.set(self.cliente_actual[8])
            email.set(self.cliente_actual[9])

        #letrero de campos obligatorios
        ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios").place(relx = 0.95, rely = 0.95, anchor = 'se')

        #nombres
        ctk.CTkLabel(master=frame_formulario,
                     text='Nombres*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=nombres,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)
        
        #apellidos
        ctk.CTkLabel(master=frame_formulario,
                     text='Apellidos*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx= (12,0), pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=apellidos,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 3, sticky = 'nsew', pady = 12)
        
        #tipo documento
        ctk.CTkLabel(master=frame_formulario,
                     text='Tipo Documento',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkComboBox(master=frame_formulario,
                        variable=tipo_doc,
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
                        values=['Cédula', 'Pasaporte']
                        ).grid(row=1, column=1, sticky = 'nsew', pady= (0,12))
        
        #numero doc
        ctk.CTkLabel(master=frame_formulario,
                     text='Numero Documento*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx= (12,0), pady = (0,12))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=numero_doc,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 3, sticky = 'nsew', pady = (0,12))
        
        #cumpleaños
        ctk.CTkLabel(master=frame_formulario,
                     text='Cumpleaños',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w',  pady = (0,12))
        cumpleanos = CTkDatePicker(master=frame_formulario)
        cumpleanos.date_entry.configure(textvariable = fecha_nac)
        cumpleanos.grid(row = 2, column = 1, sticky = 'nsew', pady = (0,12))
        cumpleanos.set_date_format('%d-%m-%Y')
        cumpleanos.set_localization('es_ES')
        cumpleanos.set_allow_manual_input(True)

        #genero
        ctk.CTkLabel(master=frame_formulario,
                     text='Género',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 2, sticky = 'w', pady = (0,12), padx= (12,0))
        ctk.CTkComboBox(master=frame_formulario,
                        variable=genero,
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
                        values=['Femenino', 'Masculino']
                        ).grid(row=2, column=3, sticky = 'nsew', pady= (0,12))
        
        #nacionalidad
        ctk.CTkLabel(master=frame_formulario,
                     text='Nacionalidad',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 3, column = 0, sticky = 'w', pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=nacionalidad,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 1, sticky = 'nsew', pady = (12,6))
        
        #telefono
        ctk.CTkLabel(master=frame_formulario,
                     text='Teléfono*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 3, column = 2, sticky = 'w', padx= (12,0), pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=telefono,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 3, sticky = 'nsew', pady = (12,6))
        
        #email
        ctk.CTkLabel(master=frame_formulario,
                     text='E-mail*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 4, column = 0, sticky = 'w', pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=email,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 4, column = 1, sticky = 'nsew', pady = (12,6))
        
        def guardar():
            #datos a guardar en formulario

            datos = [
                nombres.get().strip(),
                apellidos.get().strip(),
                tipo_doc.get().strip(),
                numero_doc.get().strip(),
                datetime.strftime(datetime.strptime(fecha_nac.get().strip(), '%d-%m-%Y'), '%Y-%m-%d'),
                genero.get().strip(),
                nacionalidad.get().strip(),
                telefono.get().strip(),
                email.get().strip()
            ]

            if not datos[0] or not datos[1] or not datos[8] or not datos[7] or not datos[3]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            #validaciones del correo electrónico
            es_valido, mensaje = self.validar_email(datos[8])
            if not es_valido:
                messagebox.showerror("Error de validación", mensaje)
                return
            
            if tipo == "agregar":
                es_valido2, mensaje2 = basedatos.email_unico(datos[8])
                if not es_valido2:
                    messagebox.showerror("Error de validación", mensaje2)
                    return

            #validación del documento de identidad
            es_valido3, mensaje3 = basedatos.doc_unico(datos[8])
            if not es_valido3:
                messagebox.showerror("Error de validación", mensaje3)
                return
            
            fue_exitoso, mensaje4 = basedatos.guardar_cliente(tipo = tipo, datos = datos)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje4)
                return
            messagebox.showinfo("Éxito", mensaje4)
            master.destroy()
            self.tabla_clientes(data=[ENCABEZADOS_CLIENTES] + [c for c in CLIENTES()])

        #boton cancelar
        ctk.CTkButton(master = frame_formulario,
                      text='Cancelar',
                      fg_color=PRIMARIO,
                      hover_color=ROJO,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=master.destroy,
                        ).grid(row = 6, column = 1, pady = 12)
        
        #boton guardar
        ctk.CTkButton(master = frame_formulario,
                      text='Guardar',
                      fg_color=VERDE1,
                      hover_color=VERDE2,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=guardar,
                        ).grid(row = 6, column = 2, pady = 12)
