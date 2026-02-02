from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(300), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
@app.route('/')
def index():
    return "hello"

@app.route('/books')
def get_books():
    books = Books.query.all()


    output = []
    for book in books:
        book_data = {'book title': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)


    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {"book title": book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Books(book_name=request.json['title'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {"id": book.id}