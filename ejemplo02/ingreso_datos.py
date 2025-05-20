from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos

# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Se lee el archivo de texto
archivo = "data/datos_clubs.txt"  
with open(archivo, "r", encoding="utf-8") as f:
    for linea in f:
        datos = linea.strip().split(";")  # Se separa la información por ;
        nombre, deporte, fundacion = datos[0], datos[1], int(datos[2])
        
        # Se crea el objeto Club y se agrega a la sesión
        club = Club(nombre=nombre, deporte=deporte, fundacion=fundacion)
        session.add(club)

# Se lee el archivo de texto con los jugadores
archivo = "data/datos_jugadores.txt"  
with open(archivo, "r", encoding="utf-8") as f:
    for linea in f:
        datos = linea.strip().split(";")  # Se separa la información por ;
        nombre_club, posicion, dorsal, nombre_jugador = datos[0], datos[1], int(datos[2]), datos[3]

        # Se busca el club en la base de datos
        club = session.query(Club).filter_by(nombre=nombre_club).first()

        if club:
            # Se crea el objeto Jugador y se agrega a la sesión
            jugador = Jugador(nombre=nombre_jugador, dorsal=dorsal, posicion=posicion, club=club)
            session.add(jugador)
        else:
            print(f"Club '{nombre_club}' no encontrado en la base de datos.")

# Se confirma la transacción
session.commit()
print("Datos de jugadores ingresados correctamente.")
