from flask import Blueprint, jsonify, request
from .models import db, Note

bp = Blueprint('notes', __name__)


@bp.get('/notes')
def list_notes():
    return jsonify([{'id': n.id, 'title': n.title, 'updated_at': n.updated_at.isoformat()} for n in Note.query.all()])


@bp.post('/notes')
def create_note():
    data = request.get_json()
    note = Note(title=data.get('title', ''), body=data.get('body', ''), notebook_id=data.get('notebook_id'))
    db.session.add(note)
    db.session.commit()
    return jsonify({'id': note.id}), 201


@bp.put('/notes/<int:note_id>')
def update_note(note_id):
    note = db.get_or_404(Note, note_id)
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.body = data.get('body', note.body)
    db.session.commit()
    return jsonify({'id': note.id})


@bp.delete('/notes/<int:note_id>')
def delete_note(note_id):
    note = db.get_or_404(Note, note_id)
    db.session.delete(note)
    db.session.commit()
    return '', 204
