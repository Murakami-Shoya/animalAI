import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import flash

from keras.models import Sequential, load_model
import keras
import numpy as np
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

classes = ["monkey", "boar", "crow"]
# クラスの数
num_classes = len(classes)
image_size = 50

def allowed_file(filename):
    # 拡張子がALLOWED_EXTENSIONSに含まれるものか
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # ファイルが存在するか
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # 正しい拡張子のファイルが存在するか
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            model = load_model('./animal_cnn_aug.h5')

            image = Image.open(filepath)
            image = image.convert("RGB")
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return classes[predicted] + ":" + str(percentage) + "%"
            # return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>upload new File</title>
    </head>
    <body>
    <h1>upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)