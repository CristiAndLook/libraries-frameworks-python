import unittest
import helpers
import copy
import database as db

class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        db.Clients.list_clients = [
            db.Client('12345678A', 'John', 'Doe'),
            db.Client('87654321B', 'Jane', 'Doe')
        ]
    
    def test_search_client(self):
        client_existing = db.Clients.search_client('12345678A')
        client_not_existing = db.Clients.search_client('11111111A')

        self.assertEqual(client_existing.name, 'John')
        self.assertEqual(client_existing.last_name, 'Doe')
        self.assertEqual(client_not_existing, None)


    def test_add_client(self):
        client = db.Clients.add_client('11111111C', 'James', 'Bond')

        self.assertEqual(client.name, 'James')
        self.assertEqual(client.last_name, 'Bond')
        self.assertEqual(len(db.Clients.list_clients), 3)

    def test_modify_client(self):
        client_to_modify = copy.copy(db.Clients.search_client('12345678A'))
        client_modified = db.Clients.modify_client(client_to_modify.dni, 'James', 'Bond')

        self.assertEqual(client_modified.name, 'James')
        self.assertEqual(client_to_modify.last_name, 'Doe')
        self.assertEqual(client_modified.last_name, 'Bond')
        self.assertEqual(len(db.Clients.list_clients), 2)

    def test_delete_client(self):
        client_to_delete = copy.copy(db.Clients.search_client('12345678A'))
        client_deleted = db.Clients.delete_client(client_to_delete.dni)

        self.assertEqual(client_deleted.name, 'John')
        self.assertEqual(client_deleted.last_name, 'Doe')
        self.assertEqual(len(db.Clients.list_clients), 1)

    def test_dni_validate(self):
        self.assertTrue(helpers.dni_validate('12345678P', db.Clients.list_clients))
        self.assertFalse(helpers.dni_validate('12345678A', db.Clients.list_clients))
        self.assertFalse(helpers.dni_validate('1234567A', db.Clients.list_clients))
    



"""
For run the test:
    1. python install pytest
    2. pytest -v
"""