""" Database models for Footnote. """

from footnote import db

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))