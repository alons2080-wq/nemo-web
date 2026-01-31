from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'nemo_704_secret'

# Configuración con tus credenciales de la imagen
SUPABASE_URL = "https://qsowpgaiqkduzgypwpww.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzb3dwZ2FpcWtkdXpneXB3cHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MTUzMjYsImV4cCI6MjA4NTM5MTMyNn0.o9hOYTdXw-yvai7XMf5-ZiIaGq5r9aogTKTgqzm8C0c" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    # Trae posts que tengan algo en video_url
    res = supabase.table('posts').select("*").not_.is_('video_url', 'null').execute()
    return render_template('videos.html', posts=res.data)

@app.route('/foro')
def foro():
    res = supabase.table('posts').select("*").order('timestamp', desc=True).execute()
    return render_template('foro.html', posts=res.data)

@app.route('/post', methods=['POST'])
def post():
    if 'user' not in session: return redirect(url_for('foro'))
    
    # Captura de datos para la tabla posts
    data = {
        "author": session['user'],
        "content": request.form.get('content'),
        "image_url": request.form.get('image_url') or None,
        "video_url": request.form.get('video_url') or None
    }
    supabase.table('posts').insert(data).execute()
    return redirect(url_for('foro'))

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form.get('username')
    return redirect(url_for('foro'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('foro'))

if __name__ == '__main__':
    app.run(debug=True)
