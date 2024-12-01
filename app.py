from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os

app = Flask(__name__, template_folder='.')  # Template folder is current directory

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Check if the uploaded file is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the file is in the request
        if 'file' not in request.files:
            return "No file part in the request", 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text from the image
            text = pytesseract.image_to_string(Image.open(filepath), lang='eng')

            # Save the extracted text to a file
            text_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.txt')
            with open(text_file, 'w') as f:
                f.write(text)

            return render_template('result.html', text=text, text_file='output.txt')

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
