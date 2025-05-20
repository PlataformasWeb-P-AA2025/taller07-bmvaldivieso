from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos

# Se genera el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Archivo de clubes
archivo_clubs = "data/datos_clubs.txt"
try:
    with open(archivo_clubs, "r", encoding="utf-8") as f:
        for linea in f:
            datos = linea.strip().split(";")
            if len(datos) == 3:  # Validación de datos
                nombre, deporte, fundacion = datos[0], datos[1], int(datos[2])
                club = Club(nombre=nombre, deporte=deporte, fundacion=fundacion)
                session.add(club)
            else:
                print(f"Datos incorrectos en línea: {linea}")
    session.commit()  # Guardar cambios después de insertar los clubes
    print("Datos de clubes ingresados correctamente.")
except Exception as e:
    print(f"Error al procesar clubes: {e}")

# Archivo de jugadores
archivo_jugadores = "data/datos_jugadores.txt"
try:
    with open(archivo_jugadores, "r", encoding="utf-8") as f:
        for linea in f:
            datos = linea.strip().split(";")
            if len(datos) == 4:  # Validación de datos
                nombre_club, posicion, dorsal, nombre_jugador = datos[0], datos[1], int(datos[2]), datos[3]
                
                # Se busca el club en la base de datos
                club = session.query(Club).filter_by(nombre=nombre_club).first()
                if club:
                    jugador = Jugador(nombre=nombre_jugador, dorsal=dorsal, posicion=posicion, club=club)
                    session.add(jugador)
                else:
                    print(f"Club '{nombre_club}' no encontrado.")
            else:
                print(f"Datos incorrectos en línea: {linea}")
    session.commit()  # Guardar cambios después de insertar los jugadores
    print("Datos de jugadores ingresados correctamente.")
except Exception as e:
    print(f"Error al procesar jugadores: {e}")
