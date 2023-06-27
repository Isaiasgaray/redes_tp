from fastapi  import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Cargamos el json en memoria
with open('datasets/books.json') as f:
    datos = json.load(f)

# Definimos la clase con la que
# vamos a recibir los libros.

class Book(BaseModel):
    author:    str
    country:   str  | None
    # imageLink: None = None
    language:  str  | None
    link:      str  | None
    pages:     int  | None
    title:     str
    year:      int  | None


@app.get('/')
def root():
    return datos

@app.post('/libros')
def add_book(book: Book):
    return book
