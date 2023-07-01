from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
import json

app = FastAPI()

PATH_DATOS = 'books.json'

BASE_URL = '/libros'

# Cargamos el json en memoria
with open(PATH_DATOS) as f:
    libros = json.load(f)

# Definimos la clase con la que
# vamos a recibir los libros.
class Book(BaseModel):
    author:    str
    country:   str  | None
    imageLink: str  | None = None
    language:  str  | None
    link:      str  | None
    pages:     int  | None
    title:     str
    year:      int  | None

class BookUpdate(Book):
    author: str | None
    title:  str | None

# Función para guardar los cambios
# en el archivo.
def guardar_cambios(archivo, datos):
    with open(archivo, 'w') as f:
        json.dump(datos, f)

# Controla que el id sea positivo.
def id_es_positivo(book_id):
    if book_id <= 0:
        raise HTTPException(
                status_code=404, 
                detail='El id debe ser un número positivo.')

# Busca un libro por su id, si lo encuentra
# devuelve su índice en la la lista y el
# libro. Si no, devuelve None.
def libro_por_id(book_id, libros):
    for idx, libro in enumerate(libros):
        if libro['id'] == book_id:
            return idx, libro
    
    return None

def error_libro_no_encontrado():
    raise HTTPException(
                status_code=404,
                detail='Libro no encontrado.'
                )

def get_libro(book_id, libros):
    id_es_positivo(book_id)
    return libro_por_id(book_id, libros)

@app.get('/')
def root():
    return libros

@app.get(BASE_URL + '/titulo/{nombre}')
def titulo(nombre: str):
    nombre = nombre.capitalize()
    for libro in libros:
        if libro["title"] == nombre:
            return libro

@app.get(BASE_URL + '/pais/{nombre}')
def paises(nombre: str):
    nombre = nombre.capitalize()
    paises = []
    for libro in libros:
        if libro["country"] == nombre:
            paises.append(libro)
    return paises

@app.get(BASE_URL + '/lenguaje/{leng}')
def lenguaje(leng: str):
    leng = leng.capitalize()
    return [libro for libro in libros if libro['language'] == leng]

@app.get(BASE_URL + '/img')
def get_img(book_id: int):

    libro = get_libro(book_id, libros)
                         
    if not libro:
        error_libro_no_encontrado()

    url_img = libro[1]['imageLink']
    img = open(url_img, 'rb')

    return StreamingResponse(img, media_type='image/png')


@app.post(BASE_URL)
def add_book(book: Book):

    libro_actualizado = book.dict()    

    ultimo_id = libros[-1]['id']

    libro_actualizado['id'] = ultimo_id + 1
    libro_actualizado['imageLink'] = None

    libros.append(libro_actualizado)

    guardar_cambios(PATH_DATOS, libros)

    return f'Libro \'{book.title}\' agregado.'

@app.delete(BASE_URL + '/{book_id}')
def delete_book(book_id: int):
    
    idx, libro = get_libro(book_id, libros)
            
    if not libro:
        error_libro_no_encontrado()

    libro_titulo = libro['title']
    libros.remove(libro)

    guardar_cambios(PATH_DATOS, libros)

    return f'Libro \'{libro_titulo}\' eliminado.'

@app.put(BASE_URL + '/{book_id}')
def update_book(book_id: int, book: BookUpdate):

    idx, libro = get_libro(book_id, libros)

    if not libro:
        error_libro_no_encontrado()

    libro_actualizado = book.dict()

    claves_no_vacias = [key for key in libro_actualizado 
                        if libro_actualizado[key]]

    for clave in claves_no_vacias:
        libros[idx][clave] = libro_actualizado[clave]

    guardar_cambios(PATH_DATOS, libros)

    return 'Libro actualizado.'

