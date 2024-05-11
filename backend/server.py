from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import subprocess
import os

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def call_hierarchy2csv(filename):
    subprocess.call(["python3", "hierarchy2csv.py", filename])

def call_viewer(viewer_filename, rankdir, from_col='node', to_col='parent', rev=True, display_col=None, group_col=None, value_col=None, all=False):
    command = [
        "python3",
        "viewer.py",
        "--f", viewer_filename,
        "--from", from_col,
        "--to", to_col,
        "--rankdir", rankdir,
        "--rev"
    ]
    subprocess.call(command)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('Saving file to:', file_path)  # Debugging: Print the file path
        try:
            file.save(file_path)
            # Process the uploaded file
            # call_hierarchy2csv(file_path)
            # call_viewer(file_path, rankdir='LR')  # Example call with default parameters
            return jsonify({'success': 'File uploaded and processed successfully'})
        except Exception as e:
            print('Error saving file:', str(e))  # Debugging: Print any errors that occur
            return jsonify({'error': 'Error saving file'})

if __name__ == "__main__":
    app.run(debug=True)
