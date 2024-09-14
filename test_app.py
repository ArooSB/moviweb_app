import unittest
from app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Users List', response.data)

    # Add more tests for different routes

if __name__ == '__main__':
    unittest.main()
