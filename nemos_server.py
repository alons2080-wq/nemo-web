from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/videos')
def videos():
    return render_template('index.html', section="videos")

@app.route('/comunidad')
def comunidad():
    return render_template('index.html', section="comunidad")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=704, debug=True)