import os
from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug import secure_filename
from detector.search import Searcher

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# create flask instance
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# main route
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            searcher = Searcher(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            results = os.path.basename(searcher.search()).split('_')[0]
            return render_template('upload.html', results=results.upper())
    return render_template('index.html')

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True,port=1880)