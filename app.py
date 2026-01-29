import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/videos')
def videos():
    # Aquí pasamos el ID del canal de Nemo para que el JS haga la magia
    return render_template('videos.html', channel_id="UCpP_S_m7_N7O0yX_D9B4w9Q")

@app.route('/directos')
def directos():
    return render_template('directos.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 704))
    app.run(host='0.0.0.0', port=port)
