import os

from flask import render_template

from footnote import app, db
from .models import Book

@app.route('/')
def index():
	return "hello"

@app.route('/book/<int:book_id>')
@app.route('/book/<int:book_id>/')
def book(book_id):
	""" Displays a book. """
	book = Book.query.get(book_id)
	return render_template("book.html",
		book_html = get_html(book_id),
		title = book.title,
	)

def get_html(book_id):
	""" Returns the HTML representation of a book. """
	path = os.path.join(app.config['BOOK_DIR'], str(book_id) + '.html')
	with open(path, 'r') as f:
		html = f.readlines()
	return "".join(html)