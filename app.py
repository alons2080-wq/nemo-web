from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'nemo_ultra_secret_704' # Cambia esto por algo aleatorio

# --- CREDENCIALES ---
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "TU_LLAVE_ANON_PUBLISHABLE_AQUI" # La que empieza por sb_publishable
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foro')
def foro():
    # Trae todos los posts para el muro de la comunidad
    try:
        res = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = res.data
    except:
        posts = []
    return render_template('foro.html', posts=posts)

@app.route('/videos')
def videos():
    # Solo trae posts que tengan video_url para la galería
    try:
        res = supabase.table('posts').select("*").not_.is_('video_url', 'null').order('timestamp', desc=True).execute()
        posts = res.data
    except:
        posts = []
    return render_template('videos.html', posts=posts)

# --- LÓGICA DE USUARIOS ---

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = supabase.table('users').select("*").eq('username', username).eq('password', password).execute()
    
    if user.data:
        session['user'] = username
        return redirect(url_for('foro'))
    return redirect(url_for('foro')) # Podrías añadir un flash de error aquí

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

# --- SUBIDA DE ARCHIVOS A SUPABASE STORAGE ---

@app.route('/post', methods=['POST'])
def post():
    if 'user' not in session:
        return redirect(url_for('foro'))

    content = request.form.get('content')
    img_file = request.files.get('image_file')
    vid_file = request.files.get('video_file')
    
    img_url = None
    vid_url = None

    def upload_to_storage(file, folder):
        if file and file.filename != '':
            filename = secure_filename(f"{session['user']}_{file.filename}")
            path = f"{folder}/{filename}"
            # Subir al bucket 'media' que debe ser PÚBLICO
            supabase.storage.from_('media').upload(path, file.read())
            return supabase.storage.from_('media').get_public_url(path)
        return None

    if img_file: img_url = upload_to_storage(img_file, "images")
    if vid_file: vid_url = upload_to_storage(vid_file, "videos")

    supabase.table('posts').insert({
        "author": session['user'],
        "content": content,
        "image_url": img_url,
        "video_url": vid_url
    }).execute()

    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
