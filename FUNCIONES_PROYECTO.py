import pandas as pd
import csv


#Creamos las funciones necesarias para desanidar los datos anidados


def desanidar_columnas(dataframe, columnas):
    desanidados = {}
    for columna in columnas:
        nueva_columna = columna + "_desanidada"
        desanidados[nueva_columna] = []
        for valor in dataframe[columna]:
            desanidados[nueva_columna].append(desanidar_valor(valor))
    return desanidados


def desanidar_valor(valor):
    if isinstance(valor, dict):
        return desanidar_diccionario(valor)
    elif isinstance(valor, list):
        return desanidar_lista(valor)
    else:
        return valor

def desanidar_diccionario(diccionario):
    desanidado = {}
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            desanidado[clave] = desanidar_diccionario(valor)
        elif isinstance(valor, list):
            desanidado[clave] = desanidar_lista(valor)
        else:
            desanidado[clave] = valor
    return desanidado

def desanidar_lista(lista):
    desanidado = []
    for elemento in lista:
        if isinstance(elemento, dict):
            desanidado.append(desanidar_diccionario(elemento))
        elif isinstance(elemento, list):
            desanidado.append(desanidar_lista(elemento))
        else:
            desanidado.append(elemento)
    return desanidado

#Creamos una función para agregar las columnas desanidadas

def agregar_columnas_desanidadas(df, columnas_anidadas):
    # Creamos una copia del DataFrame original
    df_modificado = df.copy()

    # Recorremos las columnas desanidadas y agregamos una a la vez al DataFrame copiado 'df_modificado'
    for columna in columnas_anidadas:
        valores = df_modificado[columna]
        df_modificado[columna + "_desanidada"] = pd.Series(valores)

    # Devolver el DataFrame modificado
    return df_modificado

#Creamos una función para reemplazar los valores nulos de las columnas 'budget' y 'revenue' por el valor cero

def reemplazar_nulos_por_cero(dataframe, columnas):
    dataframe[columnas] = dataframe[columnas].fillna(0)
    return dataframe


#Creamos una función para eliminar los valores nulos de una columna

def eliminar_nulos(dataframe, columnas):
    dataframe[columnas] = dataframe[columnas].dropna()
    return dataframe


#Creamos una función para eliminar las columnas que no vamos a utilizar

def eliminar_columnas(dataframe, columnas):
    dataframe.drop(columns=columnas, inplace=True)
    return dataframe

#Creamos una función para calcular el retorno y convertir las columnas "revenue" y "budget" al tipo de dato numérico

def calcular_retorno(dataframe):
    dataframe["revenue"] = pd.to_numeric(dataframe["revenue"], errors="coerce")
    dataframe["budget"] = pd.to_numeric(dataframe["budget"], errors="coerce")
    dataframe["return"] = dataframe["revenue"].div(dataframe["budget"], fill_value=0)
    return dataframe

#Creamos una función para formatear las fechas


def formatear_fechas(dataframe, columna_fecha):
    dataframe[columna_fecha] = pd.to_datetime(dataframe[columna_fecha], errors='coerce').dt.strftime('%Y-%m-%d')
    
    return dataframe




#Creamos una función para transformar los datos y quitar el .0 de los valores de las columnas

def formatear_columnas(dataframe, *columnas):
    for columna in columnas:
        dataframe[columna] = dataframe[columna].fillna(0).astype(int).astype(str)
    return dataframe


#Creamos una función para reemplazar los valores nulos o faltantes por el texto 'Información no disponible'

def reemplazar_valores_nulos(dataframe, columnas):
    dataframe[columnas] = dataframe[columnas].fillna('Información no disponible')
    return dataframe


#Creamos una función para calcular la media y usarla para reemplazar los valores nulos o faltantes

def reemplazar_valores_nulos_con_media(dataframe, columna):
    media = dataframe[columna].mean()
    dataframe[columna] = dataframe[columna].fillna(media)
    return dataframe

def limpiar_fecha(fecha):
    if fecha == "Información no disponible":
        return pd.NaT
    else:
        try:
            return pd.to_datetime(fecha, format="%Y-%m-%d")
        except ValueError:
            return pd.NaT
        
        




    
    
    
    
    
    
