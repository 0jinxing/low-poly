import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from utils.filemd5 import get_file_md5
from utils.lowploy import get_lowpoly

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['input']
        filename = secure_filename(file.filename)
        filepath = os.path.join('.', app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        filemd5 = get_file_md5(filepath)
        lowpoly_path = os.path.join(app.static_folder, filemd5 + '.' + filename.split('.')[-1])
        get_lowpoly(filepath, lowpoly_path)
        server_path = '/static/' + filemd5 + '.' + filename.split('.')[-1]
        return server_path
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
