import os
import unittest
from app import app, db
from faker import Faker

faker = Faker()
class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_endpoint_hello(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    def test_create_loja(self):
        response = self.client.post('/lojas', json={
            'descricao': faker.company()
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_produto(self):
        response = self.client.post('/produtos', json={
            'descricao': faker.text(50),
            'custo': round(faker.pydecimal(left_digits=10, right_digits=3, positive=True), 3),
            'imagem': None
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_update_produto(self):
        response = self.client.post('/produtos', json={
            'descricao': faker.text(50),
            'custo': round(faker.pydecimal(left_digits=10, right_digits=3, positive=True), 3),
            'imagem': None
        })
        produto_id = response.get_json()['id']
        response = self.client.put(f'/produtos/{produto_id}', json={
            'descricao': 'Updated Description',
            'custo': 150.00,
            'imagem': None
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Description', response.get_json()['descricao'])

    def test_delete_produto(self):
        response = self.client.post('/produtos', json={
            'descricao': faker.text(50),
            'custo': round(faker.pydecimal(left_digits=10, right_digits=3, positive=True), 3),
            'imagem': None
        })
        produto_id = response.get_json()['id']
        response = self.client.delete(f'/produtos/{produto_id}')
        self.assertEqual(response.status_code, 204)

    def test_invalid_data(self):
        response = self.client.post('/produtos', json={
            'descricao': '',
            'custo': 'not_a_number',
        })
        self.assertEqual(response.status_code, 400)

    def test_db_connection(self):
        with self.app.app_context():
            self.assertIsNotNone(db.engine)

if __name__ == '__main__':
    unittest.main()
