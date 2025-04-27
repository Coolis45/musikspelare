import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/music'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Spellistor lagras i minnet (för enkelhet)
playlists = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q', '').lower()
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    if query:
        files = [f for f in files if query in f.lower()]
    return render_template('index.html', files=files, playlists=playlists)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    name = request.form.get('playlist_name')
    if name and name not in playlists:
        playlists[name] = []
    return redirect(url_for('index'))

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    playlist = request.form.get('playlist')
    song = request.form.get('song')
    if playlist in playlists and song:
        if song not in playlists[playlist]:
            playlists[playlist].append(song)
    return redirect(url_for('index'))

@app.route('/get_playlist/<name>')
def get_playlist(name):
    return jsonify(playlists.get(name, []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 