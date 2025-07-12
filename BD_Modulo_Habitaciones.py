import sqlite3
import os # Import os module to handle file deletion for clean starts

DATABASE_NAME="base_datos.db" #

#conexion a la base de datos, la crea si no existe
def connect_db():
    try:
        conn= sqlite3.connect(DATABASE_NAME) #
        conn.row_factory=sqlite3.Row#para acceder a las columnas por nombres
        print(f"Conexion a la base de datos '{DATABASE_NAME}' realizada con correctamente.") #
        return conn #
    
    except sqlite3.Error as e: #
        print(f"Error al conectarse a la base de datos: {e}") #
        return None       #

#creacion de las tablas
def crear_tablas(): #
    # Optional: Delete existing database file to ensure a clean start for testing
    # if os.path.exists(DATABASE_NAME): # JSS: comentado porque me borró mi tabla :(
    #     os.remove(DATABASE_NAME) #
    #     print(f"Base de datos existente '{DATABASE_NAME}' eliminada para una nueva creación.") #

    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            #tabla TiposHabitacion
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TiposHabitacion(
                    id_tipo_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_tipo TEXT NOT NULL UNIQUE,
                    descripcion_tipo TEXT,
                    capacidad_default INTEGER NOT NULL,
                    precio_default REAL NOT NULL
                );
            ''') #
            #insertar tipos de habitaciones si no existen
            cursor.execute("INSERT OR IGNORE INTO TiposHabitacion (nombre_tipo, descripcion_tipo, capacidad_default, precio_default) VALUES ('Individual','Habitacion para una persona', 1, 50.0);") #
            cursor.execute("INSERT OR IGNORE INTO TiposHabitacion (nombre_tipo, descripcion_tipo, capacidad_default, precio_default) VALUES ('Doble', 'Habitacion para dos personas', 2, 80.0);") #
            cursor.execute("INSERT OR IGNORE INTO TiposHabitacion (nombre_tipo, descripcion_tipo, capacidad_default, precio_default) VALUES ('Suite', 'Habitacion de lujo con sala de estar', 4, 150);") #
            
            #tabla EstadosHabitacion
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS EstadosHabitacion(
                    id_estado_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_estado TEXT NOT NULL UNIQUE,
                    es_disponible_para_venta BOOLEAN NOT NULL, --1 para si, 0 para no
                    es_requiere_limpieza BOOLEAN NOT NULL -- Removed trailing comma
                );
            ''') #
            #insertar estados de prueba de habitacion si no existe
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Disponible', 1, 0);") #
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Ocupada', 0, 0);") #
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Sucia', 0, 1);") #
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Limpiando', 0, 0);") #
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Mantenimiento', 0, 0);") #
            cursor.execute("INSERT OR IGNORE INTO EstadosHabitacion (nombre_estado, es_disponible_para_venta, es_requiere_limpieza) VALUES ('Fuera de Servicio', 0, 0);") #

            #crear tabla Habitaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Habitaciones(
                    id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT, -- Added AUTOINCREMENT
                    numero_habitacion TEXT NOT NULL UNIQUE,
                    id_tipo_habitacion INTEGER NOT NULL,
                    id_estado_habitacion INTEGER NOT NULL,
                    ubicacion TEXT,
                    capacidad_maxima INTEGER,
                    notas_internas TEXT,
                    FOREIGN KEY(id_tipo_habitacion) REFERENCES TiposHabitacion(id_tipo_habitacion),
                    FOREIGN KEY(id_estado_habitacion) REFERENCES EstadosHabitacion(id_estado_habitacion)
                );
            ''') #
            #insertar habitaciones de prueba si no existen
            cursor.execute("INSERT OR IGNORE INTO Habitaciones (numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima) VALUES ('101', (SELECT id_tipo_habitacion FROM TiposHabitacion WHERE nombre_tipo='Doble'), (SELECT id_estado_habitacion FROM EstadosHabitacion WHERE nombre_estado='Disponible'), 'Primer Piso', 2);") #
            cursor.execute("INSERT OR IGNORE INTO Habitaciones (numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima) VALUES ('102', (SELECT id_tipo_habitacion FROM TiposHabitacion WHERE nombre_tipo='Individual'), (SELECT id_estado_habitacion FROM EstadosHabitacion WHERE nombre_estado='Ocupada'), 'Primer Piso', 1);") #
            cursor.execute("INSERT OR IGNORE INTO Habitaciones (numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima) VALUES ('201', (SELECT id_tipo_habitacion FROM TiposHabitacion WHERE nombre_tipo='Suite'), (SELECT id_estado_habitacion FROM EstadosHabitacion WHERE nombre_estado='Sucia'), 'Segundo Piso', 4);") #
            cursor.execute("INSERT OR IGNORE INTO Habitaciones (numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima) VALUES ('202', (SELECT id_tipo_habitacion FROM TiposHabitacion WHERE nombre_tipo='Doble'), (SELECT id_estado_habitacion FROM EstadosHabitacion WHERE nombre_estado='Mantenimiento'), 'Segundo Piso', 2);") #
            
            conn.commit() #
            print("Tablas creadas y datos de prueba insertados correctamente.") #
            
        except sqlite3.Error as e: #
            print(f"Error al crear las tablas o insertar datos: {e}") #
        finally:
            conn.close() #

#esta funcion recupera a todas las habitaciones con sus tipos y estados, 
#retornando una lista de diccionarios donde cada uno  representa a una habitacion
#tablas: h=habitacion, th=tipo habitacion, es=estado habitacion
def obtener_todas_habitaciones(): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('''
                SELECT
                    h.id_habitacion,
                    h.numero_habitacion,
                    th.nombre_tipo AS tipo_habitacion,
                    es.nombre_estado AS estado_habitacion,
                    es.es_disponible_para_venta,
                    es.es_requiere_limpieza,
                    h.ubicacion,
                    h.capacidad_maxima,
                    h.notas_internas
                FROM Habitaciones h
                JOIN TiposHabitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion -- Corrected table name
                JOIN EstadosHabitacion es ON h.id_estado_habitacion =  es.id_estado_habitacion
                ORDER BY h.numero_habitacion;        
            ''') #
            return [dict(row) for row in cursor.fetchall()] #
        except sqlite3.Error as e: #
            print(f"Error al obtener todas las habitaciones: {e}") #
            return [] #
        finally:
            conn.close() #
    return [] # Ensure return if conn is None
    
#funcion para obtener una sola habitacion por su id
#retorna un diccionario si la encuentra, de lo contrario, None
def obtener_habitacion_por_id(room_id): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('''
                SELECT
                     h.id_habitacion,
                    h.numero_habitacion,
                    h.id_tipo_habitacion, -- Retornar el ID para edición
                    th.nombre_tipo AS tipo_habitacion_nombre,
                    h.id_estado_habitacion, -- Retornar el ID para edición
                    es.nombre_estado AS estado_habitacion_nombre,
                    h.ubicacion,
                    h.capacidad_maxima,
                    h.notas_internas
                FROM Habitaciones h
                JOIN TiposHabitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
                JOIN EstadosHabitacion es ON h.id_estado_habitacion = es.id_estado_habitacion
                WHERE h.id_habitacion = ?;
            ''',(room_id,)) #
            row= cursor.fetchone() #
            return dict(row) if row else None #
        except sqlite3.Error as e: #
            print(f"Error al obtener la habitacion por su id: {e}") #
            return None #
        finally:
            conn.close() #
    return None # Ensure return if conn is None

#funcion para agregar una nueva habitacion a la base de datos
#retorna su id si se crea con exito y None de lo contrario
def agregar_habitacion(numero_habitacion,id_tipo_habitacion,id_estado_habitacion,ubicacion,capacidad_maxima,notas_internas): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('''
                INSERT INTO Habitaciones(numero_habitacion,id_tipo_habitacion,id_estado_habitacion,ubicacion,capacidad_maxima,notas_internas)
                VALUES (?,?,?,?,?,?);
            ''', (numero_habitacion,id_tipo_habitacion,id_estado_habitacion,ubicacion,capacidad_maxima,notas_internas)) #
            conn.commit() #
            print(f"Habitacion: '{numero_habitacion}', añadida exitosamente.") #
            return cursor.lastrowid #
        except sqlite3.IntegrityError: #
            print(f"Error al añadir la habitacion: {numero_habitacion}, el numero ya existe.") #
            return None #
        except sqlite3.Error as e: #
            print(f"Error al añadir la habitacion: {e}.") #
            return  None #
        finally:
            conn.close() #
    return None # Ensure return if conn is None

#funcion para actualizar una habitacion exisente
#retorna true/false segun el resultado
def actualizar_habitacion(room_id, numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima, notas_internas): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('''
                UPDATE Habitaciones
                SET numero_habitacion = ?,
                    id_tipo_habitacion = ?,
                    id_estado_habitacion = ?,
                    ubicacion = ?,
                    capacidad_maxima = ?,
                    notas_internas = ?
                WHERE id_habitacion = ?;
            ''', (numero_habitacion, id_tipo_habitacion, id_estado_habitacion, ubicacion, capacidad_maxima, notas_internas, room_id)) #
            conn.commit() #
            if cursor.rowcount > 0: #
                print(f"Habitacion con el ID: '{room_id}', actualizada exitosanente.") #
                return True #
            else:
                print(f"No se encontró la habitacion con el id: '{room_id}'. ") #
                return False #
        except sqlite3.IntegrityError: #
            print(f"El numero de habitacion: '{numero_habitacion}' ya existe para otra habitacion.") #
            return False #
        except sqlite3.Error as e: #
            print(f"Error al actualizar la habitacion: {e}.") #
            return False #
        finally:
            conn.close() #
    return False # Ensure return if conn is None

#funcion para actualizar el estado de una habitacion por id
#retorna true o flase
def actualizar_estado_habitacion(room_id, id_estado_habitacion): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('''
                UPDATE Habitaciones
                SET id_estado_habitacion=?
                WHERE id_habitacion=?;           
            ''',(id_estado_habitacion,room_id)) #
            conn.commit() #
            if cursor.rowcount>0: #
                print(f"Estado de la habitacion con id: '{room_id}' actualizado a estado '{id_estado_habitacion}'.") #
                return True #
            else:
                print(f"No se encontro la habitacion con el id: '{room_id}'.") #
                return False #
        except sqlite3.Error as e: #
            print(f"Error al actualizar el estado: {e} .") #
            return False #
        finally:
            conn.close() #
    return False # Ensure return if conn is None

#funcion para eliminar una habitacion de la base de datos segun su id
def eliminar_habitacion(room_id): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
            cursor.execute('DELETE FROM Habitaciones WHERE id_habitacion=?;',(room_id,)) #
            conn.commit() #
            if cursor.rowcount > 0: #
                print(f"Habitacion con id: '{room_id}' eliminada exitosamente. ") #
                return True #
            else:
                print(f"No se encontró la habitacion con el id: '{room_id}'.") #
                return False #
        except sqlite3.Error as e: #
            print(f"Error al eliminar la habitacion: {e}") #
            return False #
        finally:
            conn.close() #
    return False # Ensure return if conn is None

#funcion para recuperar los tipos de habitacion
#retorna una lista de diccionarios id_habitacion, nombre_tipo
def obtener_tipos_habitacion(): #
    conn=connect_db() #
    if conn: #
        cursor= conn.cursor() #
        try:
            cursor.execute('SELECT id_tipo_habitacion,nombre_tipo FROM TiposHabitacion;') #
            return [dict(row) for row in cursor.fetchall()] #
        except sqlite3.Error as e: #
            print(f"Error al obtener los tipos de habitacion {e}.") #
            return[] #
        finally:
            conn.close() #
    return [] # Ensure return if conn is None

#funcion para recuperar los estados de las habitaciones
#retorna una lista de diccionarios (id_estado_habitacion,nombre_estado)
def obtener_estados_habitacion(): #
    conn=connect_db() #
    if conn: #
        cursor=conn.cursor() #
        try:
           cursor.execute('SELECT id_estado_habitacion, nombre_estado FROM EstadosHabitacion;') #
           return [dict(row) for row in cursor.fetchall()] #
        except sqlite3.Error as e: #
            print(f"Error al obtener estados de habitacion: {e}. ") #
            return [] #
        finally:
            conn.close() #
    return [] # Ensure return if conn is None