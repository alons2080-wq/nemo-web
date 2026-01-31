from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

if __name__ == '__main__':
    app.run(debug=True, port=704)

