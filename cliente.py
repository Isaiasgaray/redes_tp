import requests

url = "http://localhost:8000"  # url

def menu():
    print("Elija una opción en la API")
    print("1. Agregar libro")
    print("2. Eliminar libro")
    print("3. Ver imagen del libro")
    print("4. Modificar libro")
    print("5. Ver libro por título")
    print("6. Ver libro por país")
    print("7. Ver todos los libros")
    print("8. Salir")

while True:
    menu()
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        # Agregar libro
        book_data = {
            "author": input("Autor: "),
            "country": input("Pais: "),
            "imageLink": input("Enlace de la imagen: "),
            "language": input("Idioma: "),
            "link": input("Enlace: "),
            "pages": int(input("Paginas: ")),
            "title": input("Titulo: "),
            "year": int(input("Año: "))
        }
        response = requests.post(f"{url}/libros", json=book_data)
        print(response.text)
    
    elif opcion == "2":
        # Eliminar libro
        book_id = int(input("Ingrese el ID del libro a eliminar: "))
        response = requests.delete(f"{url}/libros/{book_id}")
        print(response.text)
    
    elif opcion == "3":
        # Ver imagen del libro c:\Users\USER\Downloads
        book_id = int(input("Ingrese el ID del libro: "))
        response = requests.get(f"{url}/img/{book_id}")

        if response.status_code == 200:
                libro = response.content

                
        else:
                print("No se encontró la imagen del libro.")

    elif opcion == "4":
        # Modificar libro
        book_id = int(input("Ingrese el ID del libro a modificar: "))
        book_data = {
            "author": input("Autor (dejar en blanco si no desea modificar): "),
            "country": input("Pais (dejar en blanco si no desea modificar): "),
            "imageLink": input("Enlace de la imagen (dejar en blanco si no desea modificar): "),
            "language": input("Idioma (dejar en blanco si no desea modificar): "),
            "link": input("Enlace (dejar en blanco si no desea modificar): "),
            "pages": input("Paginas (dejar en blanco si no desea modificar): "),
            "title": input("Titulo (dejar en blanco si no desea modificar): "),
            "year": input("Año (dejar en blanco si no desea modificar): ")
        }
        # Eliminar claves con valores vacíos
        book_data = {k: v for k, v in book_data.items() if v}
        response = requests.put(f"{url}/libros/{book_id}", json=book_data)
        print(response.text)
    
    elif opcion == "5":
        # Ver libro por título
        book_title = input("Ingrese el título del libro a buscar: ")
        response = requests.get(f"{url}/titulo/{book_title}")
        if response.status_code == 200:
            book = response.json()
            print("Libro encontrado:")
            print(book)
        else:
            print("Libro no encontrado.")
    
    elif opcion == "6":
        # Ver libro por país
        book_country = input("Ingrese el pais del libro a buscar: ")
        response = requests.get(f"{url}/pais/{book_country}")
        if response.status_code == 200:
            books = response.json()
            print(books)
             
        else:
            print("No se encontraron libros para ese pais.")
    
    elif opcion == "7":
        # Ver todos los libros
        response = requests.get(f"{url}/")
        books = response.json()
        print("Todos los libros:")
        for book in books:
            print(book)
    
    elif opcion == "8":
        # Salir del programa
        print("Saliendo...")
        break

    else:
        print("Opcin invalida. Intente nuevamente.")
