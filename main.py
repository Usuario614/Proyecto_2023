
import pandas as pd
from fastapi import FastAPI
import uvicorn

# Crear una instancia de FastAPI
app = FastAPI()

meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower()
    
    if mes not in meses:
        return f"No se reconoce el mes '{mes.capitalize()}'"
    
    # Obtener el número del mes a partir del diccionario de mapeo
    numero_mes = meses[mes]
    
    # Filtrar las filas que corresponden al mes específico
    peliculas_mes = df_unidos[df_unidos['release_date'].dt.month == numero_mes]
    
    # Obtener la cantidad de películas estrenadas en el mes
    cantidad_peliculas = peliculas_mes.shape[0]
    
    # Devolver la cantidad de películas en la respuesta
    return f"{cantidad_peliculas} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"

@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    
    if dia not in ('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'):
        return f"No se reconoce el día '{dia.capitalize()}'"
    
    # Filtrar las filas que corresponden al día de la semana específico
    peliculas_dia = df_unidos[df_unidos['release_date'].apply(lambda x: obtener_dia_semana(x) == dia)]
    
    # Obtener la cantidad de películas estrenadas en el día
    cantidad_peliculas = peliculas_dia.shape[0]
    
    # Devolver la cantidad de películas en la respuesta
    return f"{cantidad_peliculas} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"

@app.get('/score_titulo')
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar la fila correspondiente al título de la filmación
    pelicula = df_unidos[df_unidos['original_title'] == titulo_de_la_filmacion]
    
    if pelicula.empty:
        return f"No se encontró la filmación con título '{titulo_de_la_filmacion}'"
    
    # Obtener el título, año de estreno y score de la película
    titulo = pelicula['original_title'].iloc[0]
    anio_estreno = pelicula['release_year'].iloc[0]
    score = pelicula['popularity'].iloc[0]
    
    # Devolver la información en la respuesta
    return f"La película {titulo} fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"

@app.get('/votos_titulo')
def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar las filas que corresponden al título de la filmación
    pelicula = df_unidos[df_unidos['original_title'] == titulo_de_la_filmacion]
    
    # Verificar si se cumplen las condiciones mínimas de votos (al menos 2000)
    cantidad_votos = int(pelicula['vote_count'].iloc[0])
    if cantidad_votos < 2000:
        return f"La película '{titulo_de_la_filmacion}' no cumple con el mínimo de 2000 votos."
    
    # Obtener el título, cantidad de votos y valor promedio de las votaciones
    titulo = pelicula['original_title'].iloc[0]
    promedio_votos = pelicula['vote_average'].iloc[0]
    
    # Devolver la información en la respuesta
    return f"La película '{titulo}' cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}."

@app.get('/get_actor')
def get_actor(nombre_actor: str):
    # Filtrar las filas que corresponden al nombre del actor
    peliculas_actor = df_unidos[df_unidos['cast'].str.contains(nombre_actor, case=False, na=False)]
    
    # Filtrar las filas que corresponden a películas en las que el actor no es director
    peliculas_actor = peliculas_actor[~peliculas_actor['crew'].str.contains(nombre_actor, case=False, na=False)]
    
    # Obtener la cantidad de películas en las que ha participado el actor
    cantidad_peliculas = peliculas_actor.shape[0]
    
    # Verificar si el actor ha participado en al menos una película
    if cantidad_peliculas == 0:
        return f"El actor {nombre_actor} no ha participado en ninguna película."
    
    # Convertir los valores de la columna 'revenue' a tipo numérico
    peliculas_actor['revenue'] = pd.to_numeric(peliculas_actor['revenue'], errors='coerce')
    
    # Eliminar las filas con valores nulos en la columna 'revenue'
    peliculas_actor = peliculas_actor.dropna(subset=['revenue'])
    
    # Calcular el retorno total del actor sumando los retornos de las películas en las que ha participado
    retorno_total = peliculas_actor['revenue'].sum()
    
    # Calcular el promedio de retorno por película
    promedio_retorno = retorno_total / cantidad_peliculas
    
    # Devolver la información en la respuesta
    return f"El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones. Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación."

@app.get("/get_director/{nombre}", tags=['Consulta 6'])
def nombre_director(nombre: str):
    # Filtrar las filas en las que el director aparece en la columna "crew_name" y "crew_job" contiene "Director"
    director_movies = df_unidos[(df_unidos['crew'].str.contains(nombre, case=False)) & (df_unidos['crew_job'] == "Director")]

    # Verificar si se encontraron películas del director
    if director_movies.empty:
        return {"mensaje": f"No se encontró al director {nombre} en la base de datos."}

    # Obtener los ID de las películas en las que el director ha trabajado
    movie_ids = director_movies['id'].tolist()

    # Filtrar el DataFrame "df_unidos" para obtener los nombres, años, presupuestos, ingresos y relación de las películas correspondientes
    movies = df_unidos[df_unidos['id'].isin(movie_ids)]

    # Calcular las ganancias sumando todas las relaciones de las películas
    ganancias = round(movies['return'].sum(), 2)

    # Crear una lista de diccionarios con los ID, nombres, años, presupuestos, ingresos y relación de las películas
    movie_info = []
    for _, row in movies.iterrows():
        movie_info.append({
            "id": row['id'],
            "titulo": row['original_title'],
            "anio": row['release_year'],
            "presupuesto": row['budget'],
            "ingresos": row['revenue'],
            "relacion": row['return']
        })

    return {
        "nombre_director": nombre,
        "ganancias": ganancias,
        "peliculas": movie_info
    }
