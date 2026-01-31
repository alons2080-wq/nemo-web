from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'nemo_704_ultra_secret_key'

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Tabla de Usuarios
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    # Tabla de Posts
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author TEXT,
                    content TEXT,
                    image_url TEXT,
                    video_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Tabla de Likes
    conn.execute('CREATE TABLE IF NOT EXISTS likes (post_id INTEGER, username TEXT)')
    # Tabla de Comentarios
    conn.execute('CREATE TABLE IF NOT EXISTS comments (post_id INTEGER, author TEXT, text TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/videos')
def videos(): return render_template('videos.html')

@app.route('/foro')
def foro():
    conn = get_db_connection()
    posts_raw = conn.execute('SELECT * FROM posts ORDER BY timestamp DESC').fetchall()
    posts = []
    for p in posts_raw:
        post_dict = dict(p)
        # Contar likes
        post_dict['likes_count'] = conn.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (p['id'],)).fetchone()[0]
        # Verificar si el usuario actual dio like
        post_dict['user_liked'] = False
        if 'user' in session:
            check_like = conn.execute('SELECT 1 FROM likes WHERE post_id = ? AND username = ?', (p['id'], session['user'])).fetchone()
            if check_like: post_dict['user_liked'] = True
        # Obtener comentarios
        post_dict['comments'] = conn.execute('SELECT * FROM comments WHERE post_id = ?', (p['id'],)).fetchall()
        posts.append(post_dict)
    conn.close()
    return render_template('foro.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    if user:
        session['user'] = username
        return redirect(url_for('foro'))
    return render_template('foro.html', error="Acceso denegado")

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        session['user'] = username
    except: pass
    conn.close()
    return redirect(url_for('foro'))

@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        content = request.form.get('content')
        img = request.form.get('image_url')
        vid = request.form.get('video_url')
        if vid: vid = vid.replace("watch?v=", "embed/")
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (author, content, image_url, video_url) VALUES (?, ?, ?, ?)',
                     (session['user'], content, img, vid))
        conn.commit()
        conn.close()
    return redirect(url_for('foro'))

@app.route('/like/<int:post_id>')
def like(post_id):
    if 'user' in session:
        conn = get_db_connection()
        exists = conn.execute('SELECT 1 FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user'])).fetchone()
        if exists:
            conn.execute('DELETE FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user']))
        else:
            conn.execute('INSERT INTO likes (post_id, username) VALUES (?, ?)', (post_id, session['user']))
        conn.commit()
        conn.close()
    return redirect(url_for('foro'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'user' in session:
        text = request.form.get('comment_text')
        if text:
            conn = get_db_connection()
            conn.execute('INSERT INTO comments (post_id, author, text) VALUES (?, ?, ?)', (post_id, session['user'], text))
            conn.commit()
            conn.close()
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
