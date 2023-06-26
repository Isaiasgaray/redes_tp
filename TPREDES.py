import requests
import json


def descargar_json(url, nombreArchivo):
    
  '''
  Descarga un archivo json.
  Como entrada pedimos url, para descargar el contedio y devolvemos el arvhivo descargado.
  '''    
  print("Descargando:", nombreArchivo)
  pagina = requests.get(url)  #Trae la página
  contenido = pagina.content  #Obtiene el contenido de la página
  print("Archivo guardado")

  with open(nombreArchivo, "w", encoding="utf-8") as archivo:  
    #Abre archivo como escritura y renombra con formato utf-8
        archivo.write(contenido.decode("utf-8"))  
  print("Descarga completa de",nombreArchivo,"\n \n")
  
libros = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json" #RAW para que te descargue el contenido
descargar_json(libros, "books.json")

def leer_archivo_json(nombre_archivo):
    
    with open(nombre_archivo, 'r') as archivo:
        datos_json = json.load(archivo)
        return datos_json
      

nombre_archivo = "books.json"
Libros = leer_archivo_json(nombre_archivo)
print(Libros)
print(len(Libros))
"""El archivo contien 100 libros y  es una lista que contiene dicionarios con clave valor. 
El diccionario contiene la informacion del libro: autor, idioma, año en el que se lanzo, pais, titulo, una imagen del libro,
cantidad de paginas, un link para mas informaciom sobre el libro.
"""
