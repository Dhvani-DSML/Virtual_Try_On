from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from utils.tryon import virtual_tryon

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ACCESSORY_FOLDER = 'static/accessories'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    accessory_type = request.form.get('accessory')
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        output_path = virtual_tryon(upload_path, accessory_type)
        return redirect(url_for('result', image_path=output_path))

@app.route('/result')
def result():
    image_path = request.args.get('image_path')
    return render_template('result.html', result_image=image_path)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
