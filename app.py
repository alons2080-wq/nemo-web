import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 704))
    app.run(host='0.0.0.0', port=port)
