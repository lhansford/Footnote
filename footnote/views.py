import os
import json

from flask import render_template, request, jsonify

from footnote import app, db
from .models import Book, Annotation

@app.route('/')
def index():
	books = {}
	for book in Book.query.all():
		if book.author in books.keys():
			books[book.author].append(book)
		else:
			books[book.author] = [book]

	return render_template("index.html",
		books = books,
		title = "Footnote",
	)

@app.route('/book/<int:book_id>')
@app.route('/book/<int:book_id>/')
def book(book_id):
	""" Displays a book and its annotations. """
	book = Book.query.get(book_id)
	annotations = [a.to_dict() for a in Annotation.query.filter_by(book=book).order_by(-Annotation.start_container, -Annotation.start_index).all()]
	return render_template("book.html",
		book = book,
		annotations = annotations,
		title = book.title,
	)

@app.route('/book/<int:book_id>/annotate', methods=['POST'])
def annotate(book_id):
	""" Receives a JSON containing a new annotation and adds it to the database. 
		Returns a JSON version of the new Annotation object.
	"""
	data = request.get_json()
	annotation = Annotation(
		# annotation = data['annotation'],
		annotated_text = data['text'],
		# start_index= data['startIndex'],
		# end_index = data['endIndex'],
		# start_container = data['startContainer'],
		# end_container = data['endContainer'],
		book = Book.query.get(book_id)
	)
	db.session.add(annotation)
	db.session.commit()
	return jsonify(annotation.to_dict())

@app.route('/book/<int:book_id>/post', methods=['POST'])
def post_html(book_id):
	""" Receives a JSON containing the new HTML for a book.
	"""
	data = request.get_json()
	book = Book.query.get(book_id)
	book.html = data['html']
	db.session.commit()
	return jsonify("")

@app.route('/book/<int:book_id>/annotations')
def get_annotations(book_id):
	book = Book.query.get(book_id)
	annotations = [a.to_dict() for a in Annotation.query.filter_by(book=book).order_by(-Annotation.start_container, -Annotation.start_index).all()]
	return jsonify(annotations)

def get_html(book_id):
	""" Returns the HTML representation of a book. """
	path = os.path.join(app.config['BOOK_DIR'], str(book_id) + '.html')
	with open(path, 'r') as f:
		html = f.readlines()
	return "".join(html)