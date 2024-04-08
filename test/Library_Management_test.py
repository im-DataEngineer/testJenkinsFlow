import os
import sys

# Add the parent directory of the app package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from app.Library_Management import app, db, Book
class TestLibraryManagementApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    @patch('app.Library_Management.render_template')
    def test_index_route(self, mock_render_template):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('index.html', books=[])

    def test_add_book_route(self):
        response = self.app.post('/add_book', data={'title': 'Test Book', 'author': 'Test Author', 'genre': 'Test Genre'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        with app.app_context():
            book = Book.query.filter_by(title='Test Book').first()
            self.assertIsNotNone(book)
            self.assertEqual(book.author, 'Test Author')
            self.assertEqual(book.genre, 'Test Genre')

    def test_borrow_book_route(self):
        with app.app_context():
            new_book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(new_book)
            db.session.commit()

            response = self.app.get(f'/borrow/{new_book.id}')
            self.assertEqual(response.status_code, 302)  # Redirect status code

            updated_book = Book.query.get(new_book.id)
            self.assertFalse(updated_book.available)

    def test_return_book_route(self):
        with app.app_context():
            new_book = Book(title='Test Book', author='Test Author', genre='Test Genre', available=False)
            db.session.add(new_book)
            db.session.commit()

            response = self.app.get(f'/return/{new_book.id}')
            self.assertEqual(response.status_code, 302)  # Redirect status code

            updated_book = Book.query.get(new_book.id)
            self.assertTrue(updated_book.available)

    def test_delete_book_route(self):
        with app.app_context():
            new_book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(new_book)
            db.session.commit()

            response = self.app.get(f'/delete/{new_book.id}')
            self.assertEqual(response.status_code, 302)  # Redirect status code

            deleted_book = Book.query.get(new_book.id)
            self.assertIsNone(deleted_book)

if __name__ == '__main__':
    unittest.main()
