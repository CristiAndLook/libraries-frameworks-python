import os
import helpers
import database as db

def start():

    while True:
        helpers.clean_screen() 

        print('''
        =======================================
            Bienvenido al Gestor de Clientes
        =======================================
        1. [1] Listar Clientes
        2. [2] Buscar Cliente
        3. [3] Anadir Cliente
        4. [4] Modificar Cliente
        5. [5] Borrar Cliente
        0. [0] Exit
        =======================================    
        ''')

        option = input("Introduce una opcion: ")

        helpers.clean_screen()

        if option == "1":
            print("Listar Clientes")
            [print(client) for client in db.Clients.list_clients]      

        elif option == "2":
            print("Buscar Cliente")
            dni = helpers.read_text(9,9, msg="Introduce el DNI del cliente 8 Números y 1 Letra: ").upper()
            client = db.Clients.search_client(dni)
            if client:
                print(client)
            else:
                print("Cliente no encontrado")

        elif option == "3":
            print("Anadir Cliente")
            dni = ""
            while True:
                dni = helpers.read_text(9,9, msg="Introduce el DNI del cliente 8 Números y 1 Letra: ").upper()
                if helpers.dni_validate(dni, db.Clients.list_clients):
                    break

            name = helpers.read_text(3,50, msg="Introduce el nombre del cliente: ").capitalize()
            last_name = helpers.read_text(3,50, msg="Introduce el apellido del cliente: ").capitalize()
            client = db.Clients.add_client(dni, name, last_name)
            print(f" Cliente {client.name} {client.last_name} añadido correctamente")

        elif option == "4":
            print("Modificar Cliente")
            dni = helpers.read_text(9,9, msg="Introduce el DNI del cliente 8 Números y 1 Letra: ").upper()
            client = db.Clients.search_client(dni)
            if client:
                name = helpers.read_text(3,50, msg="Introduce el nombre del cliente: ").capitalize()
                last_name = helpers.read_text(3,50, msg="Introduce el apellido del cliente: ").capitalize()

            client = db.Clients.modify_client(dni, name, last_name)
            print(f" Cliente {client.name} {client.last_name} modificado correctamente")

        elif option == "5":
            print("Borrar Cliente")
            dni = helpers.read_text(9,9, msg="Introduce el DNI del cliente 8 Números y 1 Letra: ").upper()
            client = db.Clients.delete_client(dni)
            if client:
                print(f" Cliente {client.name} {client.last_name} borrado correctamente")
            else:
                print("Cliente no encontrado")
        elif option == "0":
            input("\nPulsa una tecla para continuar...")
            break
        else:
            print("Opcion no valida")
            
            continue

        input("\nPulsa una tecla para continuar...")



