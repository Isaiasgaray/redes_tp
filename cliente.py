import requests

URL = 'http://localhost:8000'

try:
    requests.get(URL)
except:
    raise Exception('No se pudo abrir la URL.')

def menu():
    print("Elija una opción en la API")
    print("1. Agregar libro")
    print("2. Eliminar libro")
    print("3. Descargar imagen de libro")
    print("4. Modificar libro")
    print("5. Ver libro por título")
    print("6. Ver libro por país")
    print("7. Ver libro por idioma")
    print("8. Ver todos los libros")
    print("9. Salir")

def print_book(book):
    headers = \
        [
            ('Autor', 'author'),
            ('País', 'country'),
            ('Idioma', 'language'),
            ('Páginas', 'pages'),
            ('Título', 'title'),
            ('Año', 'year'),
            ('ID', 'id'),
        ]

    print('-' * 20)
    for atr, key in headers:
        print(f'{atr}: {book[key]}')

    print('-' * 20)
    print()


while True:
    print()
    menu()
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        # Agregar libro
        book_data = {
            "author": input("Autor: "),
            "country": input("País: "),
            # "imageLink": input("Enlace de la imagen: "),
            "language": input("Idioma: "),
            "link": input("Enlace: "),
            "pages": int(input("Páginas: ") or 0),
            "title": input("Título: "),
            "year": int(input("Año: ") or 0)
        }
        response = requests.post(f"{URL}/libros", json=book_data)
        print(f'\n{response.text}')
    
    elif opcion == "2":
        # Eliminar libro
        book_id = int(input("Ingrese el ID del libro a eliminar: "))
        response = requests.delete(f"{URL}/libros/{book_id}")
        print(f'\n{response.text}')
    
    elif opcion == "3":
        book_id = int(input("Ingrese el ID del libro: "))
        nombre = input("Ingrese el nombre para el archivo: ")

        response = requests.get(
                f"{URL}/libros/img/",
                params={'book_id': book_id}
                )

        if response.status_code != 200:
                print("\nNo se encontró la imagen del libro.")
                continue

        with open(f"{nombre}.png", "wb") as f:
            f.write(response.content)

        print("\nImagen descargada.")

    elif opcion == "4":
        # Modificar libro
        book_id = int(input("Ingrese el ID del libro a modificar: "))
        book_data = {
            "author": input("Autor (dejar en blanco si no desea modificar): "),
            "country": input("País (dejar en blanco si no desea modificar): "),
            "imageLink": input("Enlace de la imagen (dejar en blanco si no desea modificar): "),
            "language": input("Idioma (dejar en blanco si no desea modificar): "),
            "link": input("Enlace (dejar en blanco si no desea modificar): "),
            "pages": input("Páginas (dejar en blanco si no desea modificar): "),
            "title": input("Título (dejar en blanco si no desea modificar): "),
            "year": input("Año (dejar en blanco si no desea modificar): ")
        }
        # Eliminar claves con valores vacíos
        book_data = {k: v for k, v in book_data.items() if v}
        response = requests.put(f"{URL}/libros/{book_id}", json=book_data)
        print(f'\n{response.text}')
    
    elif opcion == "5":
        # Ver libro por título
        book_title = input("Ingrese el título del libro a buscar: ")
        book_title = book_title.replace(' ', '%20')
        response = requests.get(f"{URL}/libros/titulo/{book_title}")

        if response.text == 'null':
            print('\nLibro no encontrado.\n')
            continue

        book = response.json()
        print("Libro encontrado:")
        print_book(book)
    
    elif opcion == "6":
        # Ver libro por país
        book_country = input("Ingrese el país del libro a buscar: ")
        response = requests.get(f"{URL}/libros/pais/{book_country}").json()

        if not response:
            print("\nNo se encontraron libros para ese país.")
            continue

        print(f'Cantidad de libros: {len(response)}')

        for book in response:
            print_book(book)

    elif opcion == "7":
        # Ver libro por idioma
        lang = input("Ingrese el idioma del libro a buscar: ")
        response = requests.get(f"{URL}/libros/lenguaje/{lang}").json()

        if not response:
            print("\nNo se encontraron libros para ese idioma.")
            continue

        print(f'Cantidad de libros: {len(response)}')

        for book in response:
            print_book(book)
    
    elif opcion == "8":
        # Ver todos los libros
        response = requests.get(f"{URL}/")
        books = response.json()
        print("\nTotal libros: {len(response)}\nTodos los libros: ")

        for book in books:
            print_book(book)
    
    elif opcion == "9":
        # Salir del programa
        print("\nSaliendo...")
        break

    else:
        print("\nOpción inválida. Intente nuevamente.")
