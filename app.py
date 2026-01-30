import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'nemo_secret_key_704' # Clave para mantener las sesiones

# Función para verificar usuario en el archivo 'logs'
def check_user(username, password):
    if not os.path.exists('logs'): return False
    with open('logs', 'r') as f:
        for line in f:
            u, p = line.strip().split('|')
            if u == username and p == password:
                return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/foro')
def foro():
    return render_template('foro.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if check_user(username, password):
        session['user'] = username
        return redirect(url_for('foro'))
    return "Usuario o contraseña incorrectos"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # Guardar en archivo 'logs' sin extensión
    with open('logs', 'a') as f:
        f.write(f"{username}|{password}\n")
    session['user'] = username
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
