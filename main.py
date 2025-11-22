#librerias
import customtkinter as ctk #UI
from tkinter import messagebox

#ajustes y funciones
from settings import *
import basedatos
from func_clases import *

#módulos
from dashboard import *
from clientes import * 
from habitaciones import *
from reservas import *
from logistica import *
from buffet import *
from frontdesk import *
from eventos import *

class LoginDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")
        self.geometry("360x200")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.var_user = ctk.StringVar()
        self.var_pass = ctk.StringVar()

        ctk.CTkLabel(self, text="Usuario").pack(padx=16, pady=(12,0))
        ctk.CTkEntry(self, textvariable=self.var_user).pack(padx=16, fill='x')
        ctk.CTkLabel(self, text="Contraseña").pack(padx=16, pady=(8,0))
        ctk.CTkEntry(self, textvariable=self.var_pass, show="*").pack(padx=16, fill='x')
        ctk.CTkButton(self, text="Entrar", command=self._try_login).pack(pady=12)
        self.result = None

    def _try_login(self):
        user = self.var_user.get().strip()
        pw = self.var_pass.get().strip()
        auth = basedatos.autenticar_usuario(user, pw)
        if auth:
            self.result = auth
            self.destroy()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

class CreateUserDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Crear usuario")
        self.geometry("420x550")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.var_user = ctk.StringVar()
        self.var_pass = ctk.StringVar()
        self.var_pass2 = ctk.StringVar()
        self.var_nombre = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_roles = ctk.StringVar()  # roles separados por coma

        pad = {"padx": 16, "pady": 6}
        ctk.CTkLabel(self, text="Usuario").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_user).pack(fill='x', padx=16)
        ctk.CTkLabel(self, text="Contraseña").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_pass, show="*").pack(fill='x', padx=16)
        ctk.CTkLabel(self, text="Confirmar contraseña").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_pass2, show="*").pack(fill='x', padx=16)
        ctk.CTkLabel(self, text="Nombre (opcional)").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_nombre).pack(fill='x', padx=16)
        ctk.CTkLabel(self, text="Email (opcional)").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_email).pack(fill='x', padx=16)
        ctk.CTkLabel(self, text="Roles (coma separada, ej: admin,frontdesk)").pack(**pad)
        ctk.CTkEntry(self, textvariable=self.var_roles).pack(fill='x', padx=16)

        ctk.CTkButton(self, text="Crear", command=self._on_create).pack(pady=(12,16))

        self.result = None

    def _on_create(self):
        user = self.var_user.get().strip()
        pw = self.var_pass.get()
        pw2 = self.var_pass2.get()
        nombre = self.var_nombre.get().strip() or None
        email = self.var_email.get().strip() or None
        roles_raw = self.var_roles.get().strip()
        roles = [r.strip() for r in roles_raw.split(',') if r.strip()]

        if not user or not pw:
            messagebox.showerror("Error", "Usuario y contraseña son obligatorios")
            return
        if pw != pw2:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        ok, res = basedatos.crear_usuario(user, pw, nombre=nombre, email=email, roles=roles or None)
        if not ok:
            messagebox.showerror("Error al crear usuario", str(res))
            return

        messagebox.showinfo("Usuario creado", f"Usuario '{user}' creado (id={res})")
        self.result = {"id": res, "username": user, "roles": roles}
        self.destroy()

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=CLARO)

        ctk.set_appearance_mode('light')
        self.title("PMS Hotel")
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')
        
        #inicia la verificacion de las tablas de la base de datos
        basedatos.conectar_bd()
        basedatos.verificar_tablas()

        # crear tablas de autenticación si no existen
        basedatos.crear_tablas_autenticacion()
        # crear roles base
        for r in ('admin','manager','frontdesk','housekeeping','mantenimiento'):
            basedatos.crear_rol(r)

         # mostrar login modal
        dlg = LoginDialog(self)
        self.wait_window(dlg)
        if not getattr(dlg, 'result', None):
            # si no hay login válido, cerrar app
            self.destroy()
            return
        self.current_user = dlg.result
        self.current_roles = set(self.current_user.get('roles', []))
        print("Usuario activo:", self.current_user['username'], "roles:", self.current_roles)

        # acceso por módulos: map module_name -> roles allowed (si vacío => abierto)
        self.module_roles = {
            'dashboard': set(),  # abierto a todos logueados
            'clientes': {'admin','manager','frontdesk'},
            'habitaciones': {'admin','manager','mantenimiento'},
            'reservas': {'admin','frontdesk','manager'},
            'logistica': {'admin','manager'},
            'buffet': {'admin', 'manager'},
            'front': {'admin','frontdesk'},
            'eventos': {'admin','manager'},
        }

        #encabezado
        Header(self)

        #contenedor de los módulos
        self.main_frame = MainFrame(self, texto='')

        #modulos
        self.dashboard = None
        self.clientes = None
        self.habitaciones = None
        self.reservas = None
        self.logistica = None
        self.buffet = None
        self.front = None

        #menu lateral con botones
        self.sidebar = SideBar(self)

        self.btn_dashboard = self.sidebar.crear_boton_nav(BTN_HEAD[0], metodo=self.mostrar_dashboard)
        self.btn_dashboard.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_clientes = self.sidebar.crear_boton_nav(BTN_HEAD[1], metodo=self.mostrar_clientes)
        self.btn_clientes.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_habitaciones = self.sidebar.crear_boton_nav(BTN_HEAD[2], metodo=self.mostrar_habitaciones)
        self.btn_habitaciones.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_reservas = self.sidebar.crear_boton_nav(BTN_HEAD[3], metodo=self.mostrar_reservas)
        self.btn_reservas.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_front = self.sidebar.crear_boton_nav(BTN_HEAD[6], metodo=self.mostrar_front)
        self.btn_front.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)

        self.btn_eventos = self.sidebar.crear_boton_nav(BTN_HEAD[7], metodo=self.mostrar_eventos)
        self.btn_eventos.pack(fill='x', padx=6, pady=6, ipadx=16, ipady=16)

        self.btn_buffet = self.sidebar.crear_boton_nav(BTN_HEAD[5], metodo=self.mostrar_buffet)
        self.btn_buffet.pack(fill='x', padx=6, pady=6, ipadx=16, ipady=16)

        self.btn_logistica = self.sidebar.crear_boton_nav(BTN_HEAD[4], metodo=self.mostrar_logistica)
        self.btn_logistica.pack(fill='x', padx = 6, pady = 6, ipadx = 16, ipady = 16)
        
        self.btn_crear_usuario = self.sidebar.crear_boton_nav("Crear Usuario", metodo=self.mostrar_crear_usuario)
        self.btn_crear_usuario.pack(fill='x', padx=6, pady=6, ipadx=16, ipady=16)

        #cada vez que se agregue un módulo, hay que agregar su correspondiente botón y método

        #dashboard por default
        self.mostrar_dashboard()

    def _check_access(self, module_key):
        allowed = self.module_roles.get(module_key, set())
        if not allowed:
            return True
        if self.current_roles.intersection(allowed):
            return True
        messagebox.showerror("Acceso denegado", "No tienes permisos para acceder a este módulo.")
        return False

    def limpiar_mainframe(self):
        # limpia el frame que contiene los módulos
        for widget in self.main_frame.modulos.winfo_children():
            widget.destroy()

    def inactivar_botones(self):
        self.btn_dashboard.configure(fg_color = 'transparent')
        self.btn_clientes.configure(fg_color = 'transparent')
        self.btn_habitaciones.configure(fg_color = 'transparent')
        self.btn_reservas.configure(fg_color = 'transparent')
        self.btn_logistica.configure(fg_color = 'transparent')
        self.btn_buffet.configure(fg_color = 'transparent')
        self.btn_front.configure(fg_color = 'transparent')
        self.btn_eventos.configure(fg_color = 'transparent')
        self.btn_crear_usuario.configure(fg_color = 'transparent')
    
    def mostrar_dashboard(self):
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[0])
        self.btn_dashboard.configure(fg_color = '#34495e')
        self.dashboard = Dashboard(self.main_frame.modulos)

    def mostrar_clientes(self):
        if not self._check_access('clientes'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[1])
        self.btn_clientes.configure(fg_color = '#34495e')
        self.clientes = GestorClientes(self.main_frame.modulos)

    def mostrar_habitaciones(self):
        if not self._check_access('habitaciones'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[2])
        self.btn_habitaciones.configure(fg_color = '#34495e')
        self.habitaciones = GestorHabitaciones(self.main_frame.modulos)

    def mostrar_reservas(self):
        if not self._check_access('reservas'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[3])
        self.btn_reservas.configure(fg_color = '#34495e')
        self.reservas = GestorReservas(self.main_frame.modulos)

    def mostrar_front(self):
        if not self._check_access('front'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[6])
        self.btn_front.configure(fg_color = '#34495e')
        # Crear contenedor Tk puro para evitar conflictos de layout con CTk
        contenedor_front = tk.Frame(self.main_frame.modulos)
        contenedor_front.pack(fill='both', expand=True)
        # Asegurar expansión del contenedor dentro del grid del MainFrame
        try:
            contenedor_front.grid_columnconfigure(0, weight=1)
            contenedor_front.grid_rowconfigure(0, weight=1)
        except Exception:
            pass
        self.front = FrontDeskApp(contenedor_front)
    
    def mostrar_buffet(self):
        if not self._check_access('buffet'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[5])
        self.btn_buffet.configure(fg_color = '#34495e')
        self.buffet = CotizacionBuffet(self.main_frame.modulos)

    def mostrar_eventos(self):
        if not self._check_access('eventos'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[7])
        self.btn_eventos.configure(fg_color = '#34495e')
        self.eventos = CotizacionEventos(self.main_frame.modulos)

    def mostrar_logistica(self):
        if not self._check_access('logistica'):
            return
        self.limpiar_mainframe()
        self.inactivar_botones()
        self.main_frame.label_titulo.configure(text = BTN_HEAD[4])
        self.btn_logistica.configure(fg_color = '#34495e')
        self.logistica = GestorLogistica(self.main_frame.modulos)

    def mostrar_crear_usuario(self):
        if 'admin' not in getattr(self, 'current_roles', set()):
            messagebox.showerror("Acceso denegado", "Solo administradores pueden crear usuarios")
            return
        dlg = CreateUserDialog(self)
        self.wait_window(dlg)
        if getattr(dlg, 'result', None):
            # opcional: refrescar lista de usuarios u otras vistas
            print("Usuario creado:", dlg.result)

    def logout(self):
        """
        Cierra sesión y muestra el diálogo de login.
        Si el usuario cancela el login, cierra la aplicación.
        Si se autentica otro usuario, actualiza self.current_user / self.current_roles
        y vuelve al dashboard.
        """
        if not messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión actual?"):
            return
        
        # ocultar la ventana principal antes de abrir el diálogo de login
        try:
            self.withdraw()
        except Exception:
            pass

        # abrir diálogo de login
        dlg = LoginDialog(self)
        self.wait_window(dlg)
        if not getattr(dlg, 'result', None):
            # si no se autenticó nadie, cerrar la app
            self.destroy()
            return

        # actualizar sesión con nuevo usuario
        self.current_user = dlg.result
        self.current_roles = set(self.current_user.get('roles', []))
        print("Usuario activo:", self.current_user.get('username'), "roles:", self.current_roles)

        # restaurar ventana y refrescar vista / volver al dashboard
        try:
            self.deiconify()
        except Exception:
            pass

        try:
            self.limpiar_mainframe()
        except Exception:
            pass
        try:
            self.mostrar_dashboard()
        except Exception:
            pass

class Header(ctk.CTkFrame):
    def __init__(self, master, app = None):
        super().__init__(master = master, fg_color=PRIMARIO, corner_radius=0,
                         height = 43)

        self.place(x = 0, y = 0, relwidth = 1)
        self.pack_propagate(False)

        #texto encabezado
        ctk.CTkLabel(self, 
                     text='🏨 PMS Hotel · Sistema de Gestión Hotelera', 
                     text_color=BLANCO,
                     font = (FUENTE,TAMANO_TEXTO_DEFAULT,'bold'),
                     ).pack(side='left', padx = 12)
        
        self.app = app if app is not None else master

        # botón Cerrar sesión (pegado a la izquierda)
        try:
            hover_color = ROJO
        except NameError:
            hover_color = '#ff3b30'

        self.btn_cerrar_sesion = ctk.CTkButton(
            self,
            text="Cerrar sesión",
            fg_color="transparent",
            text_color="white",
            font=(FUENTE,TAMANO_TEXTO_DEFAULT, 'bold'),
            hover_color=hover_color,
            corner_radius=6,
            width=130,
            height=32,
            command=self._on_logout
        )
        self.btn_cerrar_sesion.pack(side='right', anchor='w', padx=(8,4), pady=6)

    def _on_logout(self):
        # llama al método logout() de la App si existe
        if hasattr(self.app, 'logout') and callable(getattr(self.app, 'logout')):
            self.app.logout()

class SideBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, corner_radius=0, fg_color=OSCURO, 
             width = 240)
        
        self.place(x= 0, y = 42, relheight=1)
        self.pack_propagate(False)

        #titulo del menu lateral
        ctk.CTkLabel(self, 
                     text='Módulos', 
                     text_color=BLANCO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(padx = (6+16,0+16), pady = (0+16,12+16), anchor = 'w')
    
        self.nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.nav_frame.pack(fill='both', expand=True)

    def crear_boton_nav(self, texto, metodo):
        return ctk.CTkButton(
            master = self.nav_frame,
            text=texto,
            text_color= BLANCO,
            fg_color= '#34495e',
            hover_color='#34495e',
            corner_radius=8,
            font=(FUENTE, TAMANO_TEXTO_DEFAULT),
            anchor = 'w',
            command=metodo
        )

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, texto):
        super().__init__(master=master, fg_color='transparent')
        self.place(x = 0, y = 42, relheight = 1, relwidth = 1)

        self.rowconfigure(index=1, weight=1, uniform='b')
        self.columnconfigure(index=0, weight=1, uniform='b')

        self.titulo = ctk.CTkFrame(self, fg_color=PRIMARIO,corner_radius= 10, height = 39)
        self.titulo.grid(row = 0, column = 0, sticky = 'nsew', padx = (16 + 240, 16), pady = (16,8))

        self.label_titulo =ctk.CTkLabel(self.titulo, 
                     text=texto,
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'),
                     text_color=BLANCO
                     )
        self.label_titulo.pack(side = 'left', padx = 16, pady = 6)

        #contenedor de los módulos
        self.modulos = ctk.CTkFrame(self, fg_color='transparent')
        self.modulos.grid(row = 1, column = 0, sticky = 'nsew', padx = (16 + 240, 16), pady = (8,16+43))
        self.modulos.pack_propagate(False)

if __name__ == '__main__':
    window = App()
    window.mainloop()