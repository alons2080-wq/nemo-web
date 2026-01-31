from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'nemo_secret_key_704'

# --- CONFIGURACIÓN SUPABASE ---
# Usa los datos de tu imagen image_136405.png
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    try:
        # Traemos solo posts que tengan video para la galería
        res = supabase.table('posts').select("*").not_.is_('video_url', 'null').execute()
        posts = res.data
    except:
        posts = []
    return render_template('videos.html', posts=posts)

@app.route('/foro')
def foro():
    try:
        res = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = res.data
    except:
        posts = []
    return render_template('foro.html', posts=posts)

# --- RUTA DE PUBLICACIÓN (LA QUE TE FALTABA) ---
@app.route('/post', methods=['POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('foro'))
    
    content = request.form.get('content')
    image_url = request.form.get('image_url')
    video_url = request.form.get('video_url')
    
    # Insertar en la tabla 'posts' (Estructura de image_134e33.png)
    try:
        supabase.table('posts').insert({
            "author": session['user'],
            "content": content,
            "image_url": image_url,
            "video_url": video_url
        }).execute()
    except Exception as e:
        print(f"Error al publicar: {e}")
        
    return redirect(url_for('foro'))

# --- AUTENTICACIÓN ---
@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pas = request.form.get('password')
    # Lógica simple de sesión para NEMO_704
    session['user'] = user
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
