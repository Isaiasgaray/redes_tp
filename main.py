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


@app.get('/')
def root():
    return libros

@app.get('/img')
def get_img(book_id: int):

    if book_id <= 0:
        raise HTTPException(
                status_code=404, 
                detail='El id es un número positivo.'
                )

    libro = None

    for lib in libros:
        if lib['id'] == book_id:
            libro = lib
            break 
            
    if not libro:
        raise HTTPException(
            status_code=404,
            detail='Libro no encontrado'
            )


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

    with open(PATH_DATOS, 'w') as f:
        json.dump(libros, f)    
    
    return f'Libro \'{book.title}\' agregado.'

@app.delete('/libros/{book_id}')
def delete_book(book_id: int):
    
    if book_id <= 0:
        raise HTTPException(
                status_code=404, 
                detail='El id es un número positivo.'
                )

    
    libro = None

    for lib in libros:
        if lib['id'] == book_id:
            libro = lib
            break 
            
    if not libro:
        raise HTTPException(
            status_code=404,
            detail='Libro no encontrado'
            )

    libro_titulo = libro['title']

    libros.remove(libro)

    with open(PATH_DATOS, 'w') as f:
        json.dump(libros, f)    

    return f'Libro \'{libro_titulo}\' eliminado.'

