""" Database models for Footnote. """

import json

from footnote import db

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	html = db.Column(db.Text)

class Annotation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#Annotations are in Markdown
	annotation = db.Column(db.Text)
	annotated_text = db.Column(db.Text) #This is kept in case of publication changes, not sure if necessary
	start_index= db.Column(db.Integer)
	end_index = db.Column(db.Integer)
	start_container = db.Column(db.Integer)
	end_container = db.Column(db.Integer)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	book = db.relationship('Book', backref=db.backref('annotations', lazy='dynamic'))

	def to_dict(self):
		"""Returns a dictionary representation of the Annotation object."""
		annotation = {
			'id':self.id,
			'annotation':self.annotation,
			'annotated_text':self.annotated_text,
			'start_index':self.start_index,
			'end_index':self.end_index,
			'start_container':self.start_container,
			'end_container':self.end_container,
			'book_id':self.book_id,
		}
		return annotation