from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import subprocess

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-stream', methods=['POST'])
def start_stream():
    data = request.json
    resolution = data['resolution']
    bitrate = data['bitrate']
    framerate = data['framerate']

    # Stop any existing FFmpeg processes
    subprocess.run(["pkill", "-f", "ffmpeg"], stderr=subprocess.DEVNULL)

    # Command to start live streaming with FFmpeg
    ffmpeg_command = [
    "ffmpeg",
    "-f", "v4l2",
    "-video_size", resolution,
    "-framerate", framerate,
    "-i", "/dev/video0",
    "-b:v", bitrate,
    "-c:v", "libx264",
    "-f", "hls",
    "-hls_time", "2",
    "-hls_list_size", "5",
    "-hls_flags", "delete_segments",
    "static/live.m3u8"  # Save HLS stream in the static folder
]

    try:
        subprocess.Popen(ffmpeg_command)
        return jsonify({'message': 'Stream started successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/live')
def live():
    # Serve live.m3u8 for the browser to consume
    return send_from_directory('static', 'live.m3u8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
