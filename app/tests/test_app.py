import os
import tempfile
import json
from app import app
from db import init_db, get_db

def setup_function():
    # ensure a fresh database for tests
    if os.path.exists('test_data.db'):
        os.remove('test_data.db')
    init_db('test_data.db')

def test_health():
    client = app.test_client()
    rv = client.get('/health')
    j = rv.get_json()
    assert j['status'] == 'ok'

def test_create_and_get_note():
    client = app.test_client()
    # create via API
    rv = client.post('/api/notes', json={'title':'T', 'content':'Hello world'})
    assert rv.status_code == 201
    data = rv.get_json()
    nid = data['id']
    # fetch
    rv2 = client.get(f'/api/notes/{nid}')
    assert rv2.status_code == 200
    got = rv2.get_json()
    assert got['title'] == 'T'
    assert 'Hello' in got['content']

