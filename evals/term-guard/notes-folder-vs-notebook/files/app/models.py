from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Note', backref='notebook', cascade='all, delete-orphan')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='')
    body = db.Column(db.Text, default='')
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
