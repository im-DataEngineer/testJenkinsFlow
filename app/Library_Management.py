from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Book {self.title}>'

# Routes
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    if title and author and genre:
        new_book = Book(title=title, author=author, genre=genre)
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available:
        book.available = False
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/return/<int:book_id>')
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.available:
        book.available = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
