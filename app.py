from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_nemo_704'

# --- CONEXIÓN SUPABASE ---
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    # Obtener posts que tengan video
    try:
        response = supabase.table('posts').select("*").not_.is_('video_url', 'null').order('timestamp', desc=True).execute()
        posts = response.data
    except:
        posts = []
    return render_template('videos.html', posts=posts)

@app.route('/foro')
def foro():
    # Obtener todos los posts
    try:
        response = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = response.data
    except:
        posts = []
    return render_template('foro.html', posts=posts, user=session.get('user'))

# --- RUTAS DE AUTENTICACIÓN (LOGIN/REGISTER) ---

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        # Buscamos si el usuario existe
        data = supabase.table('users').select("*").eq('username', username).eq('password', password).execute()
        if len(data.data) > 0:
            session['user'] = username # Iniciamos sesión
            return redirect(url_for('foro'))
        else:
            return redirect(url_for('foro')) # Falló login (podrías agregar mensaje de error)
    except Exception as e:
        print(f"Error login: {e}")
        return redirect(url_for('foro'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        # Crear usuario nuevo
        supabase.table('users').insert({"username": username, "password": password}).execute()
        session['user'] = username # Auto-login al registrarse
    except Exception as e:
        print(f"Error registro: {e}")
        
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

# --- RUTA PARA PUBLICAR ---

@app.route('/post', methods=['POST'])
def post():
    if 'user' not in session:
        return redirect(url_for('foro'))

    content = request.form.get('content')
    img_file = request.files.get('image_file')
    vid_file = request.files.get('video_file')
    
    img_url = None
    vid_url = None

    # Función helper para subir a Supabase Storage
    def upload_file(file, bucket_folder):
        if file and file.filename != '':
            filename = secure_filename(f"{session['user']}_{file.filename}")
            path = f"{bucket_folder}/{filename}"
            file_bytes = file.read()
            supabase.storage.from_('media').upload(path, file_bytes)
            return supabase.storage.from_('media').get_public_url(path)
        return None

    # Subimos archivos si existen
    if img_file: img_url = upload_file(img_file, "images")
    if vid_file: vid_url = upload_file(vid_file, "videos")

    # Guardamos en base de datos
    supabase.table('posts').insert({
        "author": session['user'],
        "content": content,
        "image_url": img_url,
        "video_url": vid_url
    }).execute()
    
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
