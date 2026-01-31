from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'nemo_704_ultra_secret'

# --- CONFIGURACIÓN DE SUPABASE ---
# Usa los datos de tu proyecto
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    # Solo mostramos posts que tengan una URL de video cargada
    try:
        res = supabase.table('posts').select("*").not_.is_('video_url', 'null').execute()
        posts = res.data
    except:
        posts = []
    return render_template('videos.html', posts=posts)

@app.route('/foro')
def foro():
    # Traemos todos los posts ordenados por el más reciente
    try:
        res = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = res.data
    except:
        posts = []
    return render_template('foro.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Guardamos el usuario en la sesión del navegador
    session['user'] = username
    return redirect(url_for('foro'))

@app.route('/post', methods=['POST'])
def post():
    if 'user' not in session:
        return redirect(url_for('foro'))

    # Datos extraídos del formulario profesional
    data = {
        "author": session['user'],
        "content": request.form.get('content'),
        "image_url": request.form.get('image_url') if request.form.get('image_url') else None,
        "video_url": request.form.get('video_url') if request.form.get('video_url') else None
    }
    
    try:
        supabase.table('posts').insert(data).execute()
    except Exception as e:
        print(f"Error al publicar: {e}")

    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
