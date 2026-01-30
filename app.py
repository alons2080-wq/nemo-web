import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'nemo_secret_key_704'

# Base de datos temporal para posts (se limpia al reiniciar el servidor en Render)
posts = [] 

def user_exists(username):
    if not os.path.exists('logs'): return False
    with open('logs', 'r') as f:
        for line in f:
            u, _ = line.strip().split('|')
            if u == username: return True
    return False

def check_user(username, password):
    if not os.path.exists('logs'): return False
    with open('logs', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 2:
                u, p = parts
                if u == username and p == password: return True
    return False

@app.route('/')
def home(): return render_template('index.html')

@app.route('/videos')
def videos(): return render_template('videos.html')

@app.route('/foro')
def foro():
    return render_template('foro.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if check_user(username, password):
        session['user'] = username
        return redirect(url_for('foro'))
    return "<h1>Error: Usuario o contraseña incorrectos</h1><a href='/foro'>Volver</a>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    
    if user_exists(username):
        return "<h1>Error: El nombre de usuario ya existe</h1><a href='/foro'>Intentar con otro</a>"
    
    with open('logs', 'a') as f:
        f.write(f"{username}|{password}\n")
    session['user'] = username
    return redirect(url_for('foro'))

@app.route('/post', methods=['POST'])
def create_post():
    if 'user' not in session: return redirect(url_for('foro'))
    content = request.form['content']
    if content:
        posts.insert(0, {
            'id': len(posts),
            'author': session['user'],
            'content': content,
            'likes': 0,
            'comments': []
        })
    return redirect(url_for('foro'))

@app.route('/like/<int:post_id>')
def like_post(post_id):
    for post in posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    return redirect(url_for('foro'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    if 'user' not in session: return redirect(url_for('foro'))
    text = request.form['comment']
    for post in posts:
        if post['id'] == post_id:
            post['comments'].append({'author': session['user'], 'text': text})
            break
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
