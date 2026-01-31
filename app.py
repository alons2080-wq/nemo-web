from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
# Clave para asegurar las sesiones (Login)
app.secret_key = 'nemo_704_ultra_secret_key'

SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foro')
def foro():
    try:
        # Obtenemos todos los posts ordenados por fecha (más recientes primero)
        response = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
        posts = response.data
        
        # Enriquecemos cada post con likes y comentarios
        for post in posts:
            # Conteo de Likes
            likes_res = supabase.table('likes').select("*", count='exact').eq('post_id', post['id']).execute()
            post['likes_count'] = likes_res.count if likes_res.count else 0
            
            # Verificar si el usuario actual ya dio like
            post['user_liked'] = False
            if 'user' in session:
                check = supabase.table('likes').select("*").eq('post_id', post['id']).eq('username', session['user']).execute()
                if check.data:
                    post['user_liked'] = True
            
            # Obtener Comentarios
            comm_res = supabase.table('comments').select("*").eq('post_id', post['id']).order('timestamp').execute()
            post['comments'] = comm_res.data
    except Exception as e:
        print(f"Error cargando el foro: {e}")
        posts = []
        
    return render_template('foro.html', posts=posts)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Buscamos al usuario en la tabla 'users'
    user_query = supabase.table('users').select("*").eq('username', username).eq('password', password).execute()
    
    if user_query.data:
        session['user'] = username
        return redirect(url_for('foro'))
    else:
        return render_template('foro.html', error="Usuario o contraseña incorrectos", posts=[])

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        # Insertamos nuevo usuario en Supabase
        supabase.table('users').insert({"username": username, "password": password}).execute()
        session['user'] = username
        return redirect(url_for('foro'))
    except Exception:
        return render_template('foro.html', error="El nombre de usuario ya existe o hubo un error", posts=[])

@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        content = request.form.get('content')
        img = request.form.get('image_url')
        vid = request.form.get('video_url')
        
        # Ajuste para que los videos de YouTube se vean correctamente
        if vid and "watch?v=" in vid:
            vid = vid.replace("watch?v=", "embed/")
            
        supabase.table('posts').insert({
            "author": session['user'],
            "content": content,
            "image_url": img if img else None,
            "video_url": vid if vid else None
        }).execute()
    return redirect(url_for('foro'))

@app.route('/like/<int:post_id>')
def like(post_id):
    if 'user' in session:
        # Lógica de toggle: si ya existe el like, lo borra; si no, lo crea
        check = supabase.table('likes').select("*").eq('post_id', post_id).eq('username', session['user']).execute()
        if check.data:
            supabase.table('likes').delete().eq('post_id', post_id).eq('username', session['user']).execute()
        else:
            supabase.table('likes').insert({"post_id": post_id, "username": session['user']}).execute()
    return redirect(url_for('foro'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'user' in session:
        text = request.form.get('comment_text')
        if text:
            supabase.table('comments').insert({
                "post_id": post_id,
                "author": session['user'],
                "text": text
            }).execute()
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    # Ejecución local para pruebas
    app.run(debug=True)
