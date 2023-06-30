from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
import json

app = FastAPI()

PATH_DATOS = 'books.json'

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

# Busca un libro por su id,
# si no lo encuntra devuelve none
def libro_por_id(book_id, libros):
    for libro in libros:
        if libro['id'] == book_id:
            return libro 
    
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

@app.get('/img')
def get_img(book_id: int):

    libro = get_libro(book_id, libros)
                         
    if not libro:
        error_libro_no_encontrado()

    url_img = libro['imageLink']
    img = open(url_img, 'rb')

    return StreamingResponse(img, media_type='image/png')


@app.post('/libros')
def add_book(book: Book):

    nuevo_libro = book.dict()    

    ultimo_id = libros[-1]['id']

    nuevo_libro['id'] = ultimo_id + 1
    nuevo_libro['imageLink'] = None

    libros.append(nuevo_libro)

    guardar_cambios(PATH_DATOS, libros)

    return f'Libro \'{book.title}\' agregado.'

@app.delete('/libros/{book_id}')
def delete_book(book_id: int):
    
    libro = get_libro(book_id, libros)
            
    if not libro:
        error_libro_no_encontrado()

    libro_titulo = libro['title']
    libros.remove(libro)

    guardar_cambios(PATH_DATOS, libros)

    return f'Libro \'{libro_titulo}\' eliminado.'

@app.put('/libros/{book_id}')
def update_book(book_id: int, book: BookUpdate):
    return book.dict()