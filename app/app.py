from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from db import init_db, get_db, query_db
from forms import sanitize_text
import random
import datetime

APP_NAME = "StudyBuddy"
DB_PATH = 'data.db'

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "replace-this-with-a-secret-in-prod"

# Initialize DB on startup (creates tables if not exist)
with app.app_context():
    init_db(DB_PATH)

# -----------------------
# Web routes (HTML)
# -----------------------
@app.route('/')
def index():
    notes = query_db(DB_PATH, "SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC")
    count = len(notes)
    return render_template('index.html', notes=notes, count=count, app_name=APP_NAME)

@app.route('/note/<int:note_id>')
def view_note(note_id):
    note = query_db(DB_PATH, "SELECT id, title, content, created_at FROM notes WHERE id = ?", (note_id,), one=True)
    if not note:
        flash("Note not found", "danger")
        return redirect(url_for('index'))
    # simple generated flashcards: split sentences
    sentences = [s.strip() for s in note['content'].split('.') if s.strip()]
    flashcards = []
    for i, s in enumerate(sentences[:6]):
        # make naive Q/A: hide last word
        words = s.split()
        if len(words) > 2:
            answer = words[-1].strip('.,')
            question = ' '.join(words[:-1]) + " ____"
            flashcards.append({'q': question, 'a': answer})
    return render_template('note.html', note=note, flashcards=flashcards)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = sanitize_text(request.form.get('title', 'Untitled'))
        content = sanitize_text(request.form.get('content', ''))
        if not content.strip():
            flash("Content cannot be empty", "warning")
            return redirect(url_for('create_note'))
        created_at = datetime.datetime.utcnow().isoformat()
        db = get_db(DB_PATH)
        cur = db.cursor()
        cur.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)", (title, content, created_at))
        db.commit()
        flash("Note created", "success")
        return redirect(url_for('index'))
    return render_template('note.html', note=None)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = query_db(DB_PATH, "SELECT id, title, content FROM notes WHERE id = ?", (note_id,), one=True)
    if not note:
        flash("Note not found", "danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = sanitize_text(request.form.get('title', note['title']))
        content = sanitize_text(request.form.get('content', note['content']))
        db = get_db(DB_PATH)
        db.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
        db.commit()
        flash("Note updated", "success")
        return redirect(url_for('view_note', note_id=note_id))
    return render_template('note.html', note=note)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    db = get_db(DB_PATH)
    db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    db.commit()
    flash("Note deleted", "info")
    return redirect(url_for('index'))

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('index'))
    like = f"%{q}%"
    notes = query_db(DB_PATH, "SELECT id, title, content FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC", (like, like))
    return render_template('index.html', notes=notes, count=len(notes), search=q, app_name=APP_NAME)

# -----------------------
# Minimal REST API
# -----------------------
@app.route('/api/notes', methods=['GET'])
def api_notes():
    notes = query_db(DB_PATH, "SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC")
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def api_create_note():
    payload = request.get_json() or {}
    title = sanitize_text(payload.get('title', 'Untitled'))
    content = sanitize_text(payload.get('content', ''))
    if not content:
        return jsonify({'error': 'content required'}), 400
    created_at = datetime.datetime.utcnow().isoformat()
    db = get_db(DB_PATH)
    cur = db.cursor()
    cur.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)", (title, content, created_at))
    db.commit()
    nid = cur.lastrowid
    note = query_db(DB_PATH, "SELECT id, title, content, created_at FROM notes WHERE id = ?", (nid,), one=True)
    return jsonify(note), 201

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def api_get_note(note_id):
    note = query_db(DB_PATH, "SELECT id, title, content, created_at FROM notes WHERE id = ?", (note_id,), one=True)
    if not note:
        return jsonify({'error': 'not found'}), 404
    return jsonify(note)

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def api_delete_note(note_id):
    db = get_db(DB_PATH)
    db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    db.commit()
    return jsonify({'deleted': note_id})

@app.route('/api/quiz/<int:count>', methods=['GET'])
def api_quiz(count=3):
    rows = query_db(DB_PATH, "SELECT id, title, content FROM notes")
    sentences = []
    for r in rows:
        for s in r['content'].split('.'):
            s = s.strip()
            if len(s.split()) > 3:
                sentences.append(s)
    random.shuffle(sentences)
    quiz = []
    for s in sentences[:count]:
        words = s.split()
        if len(words) > 2:
            answer = words[-1].strip('.,')
            prompt = ' '.join(words[:-1]) + ' ____'
            quiz.append({'q': prompt, 'a': answer})
    return jsonify(quiz)

@app.route('/api')
def api_docs():
    return render_template('api_docs.html')

# -----------------------
# Health
# -----------------------
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'app': APP_NAME})

# -----------------------
# Run
# -----------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

