import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Camera Streaming</h1>
    <form action="/start_stream" method="post">
        <label>Resolution:</label>
        <input type="text" name="resolution" placeholder="1280x720"><br>
        <label>Bitrate:</label>
        <input type="text" name="bitrate" placeholder="1000k"><br>
        <label>Frame Rate:</label>
        <input type="text" name="framerate" placeholder="30"><br>
        <button type="submit">Start Streaming</button>
    </form>
    <form action="/stop_stream" method="post">
        <button type="submit">Stop Streaming</button>
    </form>
    '''

@app.route('/start_stream', methods=['POST'])
def start_stream():
    resolution = request.form.get('resolution')
    bitrate = request.form.get('bitrate')
    framerate = request.form.get('framerate')
          
    # Start FFmpeg with user settings for live streaming
    os.system(f"ffmpeg \
               -f v4l2 \
               -input_format yuyv422 \
               -i /dev/video0 \
              -vcodec libx264 \
              -preset ultrafast \
              -tune zerolatency -b:v {bitrate} \
              -s {resolution} -r {framerate} \
              rtmp://localhost/live/stream")
                      
    return "Streaming started!"

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    os.system("pkill ffmpeg")
    return "Streaming stopped!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
