#DOCUMENTO LOGICA DE NEGOCIO PARA EL MODULO DE HABITACIONES
import BD_Modulo_Habitaciones #

#funcion para iniciar el modulo de habitaciones llamando a la BD
#poblando la base de datos con datos de prueba, debe ser llamada al inicio de la app principal
def iniciar_modulo_hab(): #
    BD_Modulo_Habitaciones.crear_tablas() #
    print("Modulo de habitaciones iniciado") #

#Obtiene los datos de todas las habitaciones, retornando una lista de diccionarios
def obtener_info_habitaciones(): #
    habitaciones=BD_Modulo_Habitaciones.obtener_todas_habitaciones() #
    print(f"Datos de las {len(habitaciones)} habitaciones obtenidos.") #
    return habitaciones #

#obtiene detalle de una habitacion especifica segun su id
#retorna un dicc con los detalles de dicha habitacion
def obtener_detalles_hab(room_id): #
    habitacion=BD_Modulo_Habitaciones.obtener_habitacion_por_id(room_id) #
    if habitacion: #
        print(f"Detalles de la habitacion con ID {room_id} obtenidos.") #
    else:
        print(f"Habitacion con ID {room_id} no encontrada.") #
    return habitacion #

#agrega una nueva habitacion al sistema, retorna el id si hay exito, de lo contrario None
def agregar_nueva_hab(numero_habitacion,tipo_habitacion_nombre,ubicacion,capacidad_maxima,notas_internas): #
    tipos_habitacion=BD_Modulo_Habitaciones.obtener_tipos_habitacion() #
    estados_iniciales_hab=BD_Modulo_Habitaciones.obtener_estados_habitacion() #

    id_tipo_habitacion= next((t['id_tipo_habitacion']for t in tipos_habitacion if t['nombre_tipo']==tipo_habitacion_nombre),None) # Corrected key
    id_estado_inicial= next((s['id_estado_habitacion']for s in estados_iniciales_hab if s['nombre_estado']=='Disponible'),None)# 'Disponible' es el estado por defecto para nuevas habitaciones

    if id_tipo_habitacion is None: #
        print(f"Error: el tipo de habitacion '{tipo_habitacion_nombre}' no ha sido encontrado.") #
        return None #
    if id_estado_inicial is None: #
        print("El estado inicial 'Disponible' no ha sido encontrado en la base de datos.") #
        return None #
    
    room_id= BD_Modulo_Habitaciones.agregar_habitacion(
        numero_habitacion, id_tipo_habitacion, id_estado_inicial,
        ubicacion, capacidad_maxima, notas_internas
    ) #
    if room_id: #
        print(f"Habitacion '{numero_habitacion}' agregada correctamente.") #
    else:
        print(f"Error al agregar la habitacion numero '{numero_habitacion}'.") #
    return room_id #
    
#Actualiza los datos de una habitacion existente    
def actualizar_hab_existente(room_id, numero_habitacion, tipo_habitacion_nombre, estado_habitacion_nombre, ubicacion, capacidad_maxima, notas_internas=""): #
    tipos_hab=BD_Modulo_Habitaciones.obtener_tipos_habitacion() # Corrected to get types
    estados_hab=BD_Modulo_Habitaciones.obtener_estados_habitacion() # Renamed variable for clarity

    id_tipo_hab=next((t['id_tipo_habitacion']for t in tipos_hab if t['nombre_tipo']==tipo_habitacion_nombre), None) # Corrected key
    id_estado_hab=next((s['id_estado_habitacion']for s in estados_hab if s['nombre_estado']==estado_habitacion_nombre), None) # Corrected key
    
    if id_tipo_hab is None: #
        print(f"Error: tipo de habitacion '{tipo_habitacion_nombre}' no encontrado para su actualizacion. ") #
        return False #
    if id_estado_hab is None: #
        print(f"Error: no se ha encontrado una habitacion con el estado '{estado_habitacion_nombre}' para su actualizacion.") #
        return False #
    
    exito=BD_Modulo_Habitaciones.actualizar_habitacion( room_id, numero_habitacion, id_tipo_hab, id_estado_hab,
        ubicacion, capacidad_maxima, notas_internas
    ) #
    if exito: #
        print(f"Habitacion: {room_id} actualizada.") #
    else:
        print(f"Error al actualizar la habitacion con el id: {room_id}.") #
    return exito # Return exito here
    
#Cambia el estado de una habitacion existente proporcionando su id 
#nombre_nuevo_estado (str): El nombre del nuevo estado (ej. 'Disponible', 'Sucia', 'Mantenimiento').
def cambiar_estado_hab(room_id,nombre_nuevo_estado): #
    estados_hab=BD_Modulo_Habitaciones.obtener_estados_habitacion() #
    id_nuevo_estado_hab=next((s['id_estado_habitacion']for s in estados_hab if s['nombre_estado']==nombre_nuevo_estado ), None) # Corrected key

    if id_nuevo_estado_hab is None: #
        print(f"Error: el estado '{nombre_nuevo_estado}' no es valido o no existe. ") #
        return False #
    
    exito=BD_Modulo_Habitaciones.actualizar_estado_habitacion(room_id,id_nuevo_estado_hab) #

    if exito: #
        print(f"El estado de la habitacion con el ID: '{room_id}' ha sido actualizado a '{nombre_nuevo_estado}'. ") # Changed to use nombre_nuevo_estado for clarity
    else:
        print(f"Error al actualizar el estado de la habitacion con el ID: '{room_id}'. ") #
    return exito # Return exito here

#Elimina una habitacion del sistema mediante el id proporcionado
def eliminar_habitacion(room_id): #
    exito=BD_Modulo_Habitaciones.eliminar_habitacion(room_id) #

    if exito: #
        print(f"Habitacion el ID: '{room_id}' eliminada con exito.") #
    else:
        print(f"Error al intentar eliminar la habitacion con el ID: '{room_id}'.") #
    return exito # Return exito here

#Obtiene los nombres y IDs de los tipos de habitaciones disponibles
#retorna lista de diccionarios (nombre_tipo_ y id_tipo_habitacion)
def obtener_tipos_hab_disponible(): #
    return BD_Modulo_Habitaciones.obtener_tipos_habitacion() #

#Obtiene los nombres y IDs de los estados de las habitaciones disponibles
#retorna una lista de diccionarios (id_estado_habitacion y nombre_estado)
def obtener_estado_hab_disponible(): #
    return BD_Modulo_Habitaciones.obtener_estados_habitacion() #