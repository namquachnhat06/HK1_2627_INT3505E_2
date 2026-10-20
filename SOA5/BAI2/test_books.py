import unittest
from app import app
from models import db

class BookApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_list_books_offset(self):
        # Test offset strategy
        response = self.app.get('/api/v1/books?strategy=offset')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pagination', response.json)
        self.assertEqual(response.json['pagination']['strategy'], 'offset')

    def test_list_books_cursor(self):
        # Test cursor strategy
        response = self.app.get('/api/v1/books?strategy=cursor')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pagination', response.json)
        self.assertEqual(response.json['pagination']['strategy'], 'cursor')

if __name__ == '__main__':
    unittest.main()