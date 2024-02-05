import csv
import config
class Client:
    def __init__(self, dni, name, last_name):
        self.dni = dni
        self.name = name
        self.last_name = last_name

    def __str__(self):
        return f'{self.dni} | {self.name} | {self.last_name}'
    
class Clients:

    list_clients = []
    with open(config.DATABASE_PATH, newline='\n') as file:
        reader = csv.reader(file, delimiter=';')
        for dni, name, last_name in reader:
            list_clients.append(Client(dni, name, last_name))

    @staticmethod
    def search_client(dni):
        for client in Clients.list_clients:
            if client.dni == dni:
                return client
    
    @staticmethod
    def add_client(dni, name, last_name):
        client = Client(dni, name, last_name)
        Clients.list_clients.append(client)
        Clients.save_clients()
        return client
    
    @staticmethod
    def modify_client(dni, name, last_name):
        client = Clients.search_client(dni)
        client.name = name
        client.last_name = last_name
        Clients.save_clients()
        return client
    
    @staticmethod
    def delete_client(dni):
        client = Clients.search_client(dni)
        Clients.list_clients.remove(client)
        Clients.save_clients()
        return client    

    @staticmethod
    def save_clients():
        with open(config.DATABASE_PATH, 'w', newline='\n') as file:
            writer = csv.writer(file, delimiter=';')
            for client in Clients.list_clients:
                writer.writerow([client.dni, client.name, client.last_name])    