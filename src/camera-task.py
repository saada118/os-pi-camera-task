import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_stream')
def start_stream():
    os.system("ffmpeg command to start stream")  # Replace with the actual command
    return "Stream started!"

@app.route('/stop_stream')
def stop_stream():
    os.system("pkill ffmpeg")
    return "Stream stopped!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
