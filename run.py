# pip install Flask
# pip install Werkzeug

import logging
import uuid
import random  # Import the random module
from flask import Flask, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_route():
    # Generate a random route using a UUID
    return str(uuid.uuid4())

@app.route('/<random_route>', methods=['GET', 'POST'])  # Use a variable for the route
def upload_file(random_route):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Log the route and uploaded file
            logging.info(f"Route: /{random_route}, Uploaded file: {filename}")

            return 'File uploaded successfully'
    
    # Log the route even for GET requests
    logging.info(f"Route: /{random_route}")

    return '''
    <!doctype html>
    <title>Upload .zip File</title>
    <h1>Upload .zip File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Set up logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=8080)
