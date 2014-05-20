import os

from footnote import app, db
from footnote.models import Book

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
		db.session.add(book)
		db.session.commit()

add_books()
