import os

from footnote import app, db
from footnote.models import Book, Author

def add_books():
	directory = app.config['BOOK_DIR']
	for path in os.listdir(directory):
		if path == ".DS_Store":
			continue
		print(path)
		book = Book()
		enc='iso-8859-1'
		with open(os.path.join(directory,path),'r',encoding=enc) as f:
			html = f.readlines()
		html = "".join(html)
		body_start = html.find("<body>")
		if body_start == -1:
			body_start = html.find("<BODY>")
		body_end = html.find("</body>", body_start)
		if body_end == -1:
			body_end = html.find("</BODY>", body_start)
		book.html = html[body_start+6:body_end]
		title_start = html.find("Title:")
		title_end = html.find("\n", title_start)
		book.title = html[title_start+6:title_end].strip()
		author_start = html.find("Author:")
		author_end = html.find("\n", author_start)
		author_name = html[author_start+7:author_end].strip()
		book.author = get_author(author_name)
		db.session.add(book)
		db.session.commit()

def get_author(name):
	author = Author.query.filter_by(name=name).first()
	if(not author):
		author = Author(name=name)
		db.session.add(author)
		db.session.commit()
	return author


add_books()
