import requests
import json

URL_BASE = 'https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json'
NOMBRE_ARCHIVO = 'books.json'

r = requests.get(URL_BASE)

if r.status_code != 200:
    raise Exception('No se pudo descargar el archivo.\nStatus code != 200')

libros = r.json()

# Agrega un identificador único a cada entrada
for idx, libro in enumerate(libros):
    libro['id'] = idx + 1

with open(NOMBRE_ARCHIVO, 'w') as f:
    json.dump(libros, f)
