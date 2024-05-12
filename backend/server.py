from flask import Flask, render_template, request, jsonify, url_for, send_file
from werkzeug.utils import secure_filename
import subprocess
import os
import time
import json

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = '../downloads'

def strip_extension(filename):
    # Split the filename by dot (.)
    parts = filename.split('.')
    # If there is an extension, remove it
    if len(parts) > 1:
        return '.'.join(parts[:-1])  # Join all parts except the last one (the extension)
    else:
        return filename  # No extension found, return the original filename
        
def call_viewer(viewer_filename, rankdir):
    command = [
        "python3",
        "./viewer.py",  
        viewer_filename,
        rankdir
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    output = json.loads(result.stdout.strip())
    return output

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
        # Get filename without extension
        filename_without_extension = strip_extension(secure_filename(file.filename))
        timestamp = int(time.time())  # Get current timestamp
        filename_with_timestamp = f"{filename_without_extension}_{timestamp}"  # Append timestamp to filename without extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp)
        print('Saving file to:', file_path)  # Debugging: Print the file path
        print()
        print(f"Input filename to viewer: {filename_with_timestamp}")
        print()
        try:
            file.save(file_path)
            # Process the uploaded file
            output = call_viewer(filename_with_timestamp, rankdir='LR')
            return jsonify({'success': 'File uploaded and processed successfully',
                            'download_png': output["png_download"],
                            'download_html': output["html_download"],
                            'download_json': output["json_download"],
                            'download_magjac': output['magjac_download']})
            
        except Exception as e:
            print('Error saving file:', str(e))  # Debugging: Print any errors that occur
            return jsonify({'error': 'Error saving file'})

# Route for downloading a generated file
@app.route('/downloads/<filename>')
def download_file(filename):
    generated_file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(generated_file_path):
        if filename.endswith('.html'):
            return send_file(generated_file_path, as_attachment=False)
        else:
            return send_file(generated_file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'})

if __name__ == "__main__":
    app.run(debug=True)
