from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'nemo_704_secret_key'

# --- CONFIGURACIÓN DE SUPABASE ---
# Usa los datos de tus capturas anteriores
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foro')
def foro():
    try:
        response = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = response.data
        for post in posts:
            likes = supabase.table('likes').select("*", count='exact').eq('post_id', post['id']).execute()
            post['likes_count'] = likes.count if likes.count else 0
            post['comments'] = supabase.table('comments').select("*").eq('post_id', post['id']).execute().data
    except:
        posts = []
    return render_template('foro.html', posts=posts, title="COMUNIDAD")

@app.route('/videos')
def videos():
    try:
        # Filtramos solo los posts que tienen video_url
        response = supabase.table('posts').select("*").not_.is_('video_url', 'null').order('timestamp', desc=True).execute()
        posts = response.data
    except:
        posts = []
    return render_template('foro.html', posts=posts, title="GALERÍA DE VIDEOS")

@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        content = request.form.get('content')
        image_file = request.files.get('image_file')
        video_file = request.files.get('video_file')
        
        img_url = None
        vid_url = None

        # Función interna para subir archivos al Storage
        def upload_media(file, folder):
            if file and file.filename != '':
                filename = secure_filename(f"{session['user']}_{file.filename}")
                path = f"{folder}/{filename}"
                # Subir al bucket 'media'
                content_bytes = file.read()
                supabase.storage.from_('media').upload(path, content_bytes)
                # Retornar URL pública
                return supabase.storage.from_('media').get_public_url(path)
            return None

        img_url = upload_media(image_file, "images")
        vid_url = upload_media(video_file, "videos")

        supabase.table('posts').insert({
            "author": session['user'],
            "content": content,
            "image_url": img_url,
            "video_url": vid_url
        }).execute()
        
    return redirect(url_for('foro'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = supabase.table('users').select("*").eq('username', username).eq('password', password).execute()
    if user.data:
        session['user'] = username
        return redirect(url_for('foro'))
    return redirect(url_for('foro'))

@app.route('/register', methods=['POST'])
def register():
    u, p = request.form.get('username'), request.form.get('password')
    try:
        supabase.table('users').insert({"username": u, "password": p}).execute()
        session['user'] = u
    except: pass
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
