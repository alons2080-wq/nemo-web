import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'nemo_ultra_secret_704'

# Simulación de base de datos (Se reinicia al apagar el server en Render)
posts = []

def user_exists(username):
    if not os.path.exists('logs'): return False
    with open('logs', 'r') as f:
        for line in f:
            if line.strip():
                u, _ = line.strip().split('|')
                if u == username: return True
    return False

def check_user(username, password):
    if not os.path.exists('logs'): return False
    with open('logs', 'r') as f:
        for line in f:
            if line.strip():
                u, p = line.strip().split('|')
                if u == username and p == password: return True
    return False

@app.route('/')
def home(): return render_template('index.html')

@app.route('/videos')
def videos(): return render_template('videos.html')

@app.route('/foro')
def foro(): return render_template('foro.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    u, p = request.form['username'], request.form['password']
    if check_user(u, p):
        session['user'] = u
        return redirect(url_for('foro'))
    return "<h1>Error: Login fallido</h1><a href='/foro'>Volver</a>"

@app.route('/register', methods=['POST'])
def register():
    u, p = request.form['username'].strip(), request.form['password'].strip()
    if user_exists(u): return "<h1>Error: Usuario ya existe</h1><a href='/foro'>Volver</a>"
    with open('logs', 'a') as f: f.write(f"{u}|{p}\n")
    session['user'] = u
    return redirect(url_for('foro'))

@app.route('/post', methods=['POST'])
def create_post():
    if 'user' in session:
        content = request.form['content']
        posts.insert(0, {'id': len(posts), 'author': session['user'], 'content': content, 'likes': 0, 'comments': []})
    return redirect(url_for('foro'))

@app.route('/like/<int:post_id>')
def like_post(post_id):
    for p in posts:
        if p['id'] == post_id: p['likes'] += 1; break
    return redirect(url_for('foro'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    if 'user' in session:
        text = request.form['comment']
        for p in posts:
            if p['id'] == post_id: p['comments'].append({'author': session['user'], 'text': text}); break
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
