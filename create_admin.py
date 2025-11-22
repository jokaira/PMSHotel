#correr esto si se inicia desde cero, para generar una cuenta con rol de admin, quien administraría el sistema. Se corre en consola.

import getpass
import basedatos

def main():
    basedatos.crear_tablas_autenticacion()
    username = input("Usuario admin a crear (ej: admin): ").strip() or "admin"
    if basedatos.usuario_existe(username):
        print("El usuario ya existe.")
        return
    pwd = getpass.getpass("Contraseña: ")
    pwd2 = getpass.getpass("Confirmar contraseña: ")
    if pwd != pwd2:
        print("Contraseñas no coinciden.")
        return
    ok, res = basedatos.crear_usuario(username, pwd, nombre="Administrador", email=None, roles=['admin'])
    if ok:
        print("Usuario creado id =", res)
    else:
        print("Error creando usuario:", res)

if __name__ == "__main__":
    main()