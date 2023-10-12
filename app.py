from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.processing import processing_images
import os

# Server settings
app = Flask(__name__)
CORS(app)

# Allowed file formats
ALLOWED_FORMATS = ['.tiff', '.tif', '.jpeg', '.jpg']

# Routes
@app.route('/')
def index():
    return 'Welcome to my API Gulupa!'

# Route to upload images
@app.route('/upload', methods=['POST'])
def upload():
    # Check if the request contains a files
    if 'files' not in request.files:
        return jsonify({'error': 'No hay archivos cargados'}), 400
    # Save files in uploads folder if have the right extension
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    for file in request.files.getlist('files'):
        if os.path.splitext(file.filename)[1].lower() in ALLOWED_FORMATS:
            file.save(f'uploads/{file.filename}')
            print(f'file {file.filename} saved')
        else:
            for file in os.listdir('uploads'):
                os.remove(os.path.join('uploads', file))
            return jsonify({'error': 'Imágenes con extensión incorrecta'}), 400
    # Estimation of nitrogen
    nitrogen = processing_images()
    # remove images from uploads folder
    for file in os.listdir('uploads'):
        os.remove(os.path.join('uploads', file))
    # Send result
    return jsonify({'nitrogen': nitrogen}), 200

if __name__ == '__main__':
  app.run(debug=True)