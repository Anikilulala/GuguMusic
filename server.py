import os
import uuid
import glob
from mutagen.mp3 import MP3
from flask import Flask, flash, json, redirect, url_for
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024
app.config['SECRET_KEY'] = uuid.uuid4().hex


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        for file in request.files.getlist('file'):
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # if user does not select file, browser also
            # submit an empty part without filename

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))            
            else:
                flash('Only support MP3')
                return redirect(request.url)
        flash('Done')
        return redirect(request.url)

    return render_template('upload.html')


@app.route('/', methods=['GET'])
def index():
    result = []
    for file_path in glob.glob(os.path.join(UPLOAD_FOLDER, '*.mp3')):
        try:
            duration = MP3(file_path).info.length
        except Exception as e:
            continue

        file_name = os.path.basename(file_path)

        result.append({
            'name': file_name,
            'url': url_for('static', filename="upload/" + file_name),
            'duration': duration
        })
    return json.jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000",debug=True)
