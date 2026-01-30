from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# Sin esta clave, las sesiones de login darán error siempre
app.secret_key = 'nemo_704_ultra_secret_key'

# Base de datos temporal (En el futuro podrías usar SQL)
users = {} 
posts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/foro')
def foro():
    return render_template('foro.html', posts=posts)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and username not in users:
        users[username] = password
        session['user'] = username
    return redirect(url_for('foro'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Verificamos si el usuario existe y la contraseña coincide
    if username in users and users[username] == password:
        session['user'] = username
        return redirect(url_for('foro'))
    else:
        # Si falla, recargamos con un mensaje simple
        return render_template('foro.html', error="Credenciales incorrectas", posts=posts)

@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        content = request.form.get('content')
        if content:
            posts.insert(0, {'author': session['user'], 'content': content})
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
