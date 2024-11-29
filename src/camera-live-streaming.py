from flask import Flask, request, jsonify, send_from_directory, render_template
import subprocess

app = Flask(__name__)

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
        "-f", "mpegts",
        "udp://127.0.0.1:12345"
    ]

    try:
        subprocess.Popen(ffmpeg_command)
        return jsonify({'message': 'Stream started successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/live')
def live():
    # Proxy the video stream
    return send_from_directory('.', 'live.m3u8')  # Replace with actual stream path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
