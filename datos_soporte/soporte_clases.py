
from IPython.core.interactiveshell import InteractiveShell # Nos permite mostar más de una salida por celda
InteractiveShell.ast_node_interactivity = "all" # Nos permite mostar más de una salida por celda

import requests
import pandas as pd
import numpy as np
import mysql.connector
from geopy.geocoders import Nominatim


class Extraccion:

    """
    Clase que contiene diferentes métodos para llamar a la api y unir los diferentes dataframes
    obtenidos de la previa llamada.
    """

    def __init__(self):

        self = self
    
    def llamada_api(self, pais):

        """Primer método que recibe como parámetro el nombre del país del que se quiere
        obtener información de la API. El parámetro es de tipo string.
        """

        self.pais = pais
        
        lista_pais = ['Argentina', 'Canada', 'United States']        

        if pais not in lista_pais:
            
            return "No es posible extraer información del país que solicita"

        else:

            response = requests.get(f'http://universities.hipolabs.com/search?country={pais}')

            response.status_code

            response.reason

            df_pais = pd.json_normalize(response.json())
        
            return df_pais
        

    def union_dataframe(self, lista_dataframes):

        """Segundo método que recibe como parámetro una lista de dataframes para unir."""

        self.lista_dataframes = lista_dataframes
        
        df_unido = pd.concat(lista_dataframes, axis= 0, join = 'outer')
        return df_unido
    

class Limpieza:
    """Clase que tiene como objetivo la limpieza y procesado
     de algunos cambios aplicados al dataframe"""
    def __init__(self):

        self = self
    
    def cambiar_guion(dataframe):
        """Método que permite sustituir un guion intermedio "-" por uno bajo "_. Recibe un parámetro,
    que es un dataframe."""
        nuevas_col = {col:col.replace("-", "_") for col in df.columns}
        dataframe.rename(columns = nuevas_col,inplace = True)
        return dataframe
    
    def reemplazo_none(dataframe):
        """Método que permite reemplazar los elementos None por Nan.Recibe como parámetro el dataframe
    sobre el que se quieren aplicar los cambios."""
        dataframe = dataframe.fillna(value = np.nan, axis=1)
        return dataframe 
    
    def reemplazo_desconocido(dataframe, columna):
        """Método que permite sustituir los Nan por el string "Unknown". Recibe dos parámetros: 
    el dataframe y la columna sobre la que se quiere realizar el cambio. """
        dataframe[columna].fillna("Unkwnon", inplace=True)
        return dataframe
    
    def cambiar_estado(dataframe, columna, diccionario):
        """Método que tiene como objetivo reemplazar los valores únicos de una columna. Recibe tres parámetros:
    el dataframe, la columna sobre la que se quieren cambiar los valores y el diccionario con los nuevos valores asignados."""
        dataframe[columna]=dataframe[columna].map(diccionario)
        dataframe[columna].replace(np.nan, "Unkwnon", inplace=True)
        return dataframe
    
    def obtener_coordenadas(lista_unicos_provincia):
        """Método que permite obtener las coordenadas de latitud y longitud de cualquier lugar que se le pase.
    Recibe un parámetro, que es una lista con lugares, sitios, localizaciones."""
        lista_coordenadas = []
        geolocator = Nominatim(user_agent="mi_usuario")
        
        for provincia in lista_unicos_provincia:
            if provincia == "Unkwnon":
                lista_coordenadas.append(("Unkwnon", "Unkwnon"))
            else:
                ubicacion = geolocator.geocode(provincia)
                coordenadas = (ubicacion.latitude, ubicacion.longitude)
                lista_coordenadas.append(coordenadas)
        return lista_coordenadas
    
    def mergear_tablas(dataframe1, dataframe2, columna):
        """Método que sirve para mergear tablas que tienen alguna columna en común. Recibe tres parámetros: los
    dataframes que se quieren unir y la columna por la que se quiere realizar la unión. Este último parámetro es
    de tipo string."""
        df_final = dataframe1.merge(dataframe2, on = columna, how= 'inner' )
        return df_final


    class Bbdd():

        """Clase que cuenta con métodos enfocados en la creación de BBDD, creación de tablas e 
        inserción de datos en la misma, así como diferentes métodos para poder extraer los id que son clave foránea
        y que la inserción de los datos se realice satisfactoriamente."""

        def __init__(self, nombre_bbdd, contraseña):
                # nuestra clase va a recibir dos parámetros que son fijos a lo largo de toda la BBDD, el nombre de la BBDD y la contraseña con el servidor. 
                self.nombre_bbdd = nombre_bbdd
                self.contraseña = contraseña


        def crear_bbdd(self):
                
                """Primer método. Sirve para crear la BBDD. No recibe parámetros"""

                mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="AlumnaAdalab", 
                                        auth_plugin = 'mysql_native_password') 
                print("Conexión realizada con éxito")
                
                mycursor = mydb.cursor()

                try:
                        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};")
                        print(mycursor)
                except mysql.connector.Error as err:
                        print(err)
                        print("Error Code:", err.errno)
                        print("SQLSTATE", err.sqlstate)
                        print("Message", err.msg)
                        

        def crear_insertar_tabla(self, query):
                
                """"Segundo método. Tiene como objetivo la creación de tabla, así como la inserción de datos en la misma.
                Recibe un parámetro, la query que queramos realizar, sea de creación o de inserción.
                """
                self.query = query
    
                cnx = mysql.connector.connect(user='root', password=f"{self.contraseña}",
                                                host='127.0.0.1', database=f"{self.nombre_bbdd}",  
                                                auth_plugin = 'mysql_native_password')
                
                mycursor = cnx.cursor()
                
                
                try: 
                        mycursor.execute(query)
                        cnx.commit() 
                
                except mysql.connector.Error as err:
                        print(err)
                        print("Error Code:", err.errno)
                        print("SQLSTATE", err.sqlstate)
                        print("Message", err.msg)


        def check_paises(self):
                
                """Tercer método. Tiene como objetivo verificar que ya hay países en la tabla antes de insertar.
                No recibe parámetros."""
        
                mydb = mysql.connector.connect(user='root',
                                        password=f"{self.contraseña}",
                                        host='127.0.0.1',
                                        database=f"{self.nombre_bbdd}")
                mycursor = mydb.cursor()

                # query para extraer los valores únicos de ciudades de la tabla de paises 
                query_existe_pais = f"""
                        SELECT DISTINCT nombre_pais FROM paises
                        """
                mycursor.execute(query_existe_pais)
                paises = mycursor.fetchall()
                return paises

        def sacar_id_pais(self, pais):
                
                """Cuarto método. Sirve para obtener el id de país para poder utilizarlo en la inserción de la segunda tabla,
                donde id pais es FK. Tiene un parámetro, que es de tipo string y correponde con el nombre del país del cual se
                quiere obtener el id."""

                self.pais = pais

                mydb = mysql.connector.connect(user='root',
                                        password= f'{self.contraseña}',
                                        host='127.0.0.1', 
                                        database=f"{self.nombre_bbdd}")
                mycursor = mydb.cursor()
                
                try:
                        query_sacar_id_pais = f"SELECT idestado FROM paises WHERE nombre_pais = '{pais}'"
                        mycursor.execute(query_sacar_id_pais)
                        id_pais = mycursor.fetchall()[0][0]
                        return id_pais
                
                except: 
                        return "Lo sentimos, no tenemos ese país en la BBDD y por lo tanto no te podemos facilitar su id." 


        def sacar_id_universidad(self,nombre_universidad):
                
                """Quinto método. Sirve para obtener el id de la universidad. Recibe un parámetro: el nombre de la
                universidad, que es de tipo string."""

                self.nombre_universidad = nombre_universidad

                mydb = mysql.connector.connect(user='root', password=f'{self.contraseña}',
                                                host='127.0.0.1', database=f"{self.nombre_bbdd}")
                mycursor = mydb.cursor()

                try:
                        query_sacar_id_uni = f"SELECT iduniversidades FROM universidades WHERE nombre_universidad = '{nombre_universidad}'"
                        mycursor.execute(query_sacar_id_uni)
                        id_uni = mycursor.fetchall()[0][0]
                        return id_uni
                
                except: 
                        return "Lo sentimos, no tenemos esa universidad en la BBDD y por lo tanto no te podemos facilitar su id." 