# /backend/server.py
import logging
from flask import Flask, render_template, request, jsonify, url_for, send_file
from werkzeug.utils import secure_filename
import subprocess
import os
import time
import json
import user_agents

# Configure Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

# Configure logging
log_file_path = '/var/log/flask.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = '../downloads'
METRICS_LOG_FILE = '/var/log/metrics.log'  # Path to metrics log file


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
    output = result.stdout.strip()
    logging.info(f'Viewer output: {output}')
    if output:
        try:
            json_output = json.loads(output)  # Attempt to parse the output as JSON
            return json_output
        except json.JSONDecodeError as e:
            logging.error(f'Error parsing viewer output as JSON: {e}')
            return None
    else:
        logging.error('Viewer output is empty')
        return None

def parse_user_agent(user_agent_string):
    user_agent = user_agents.parse(user_agent_string)
    os_info = user_agent.os.family + ' ' + user_agent.os.version_string
    device_info = user_agent.device.family
    return os_info, device_info

# Function to log metrics to metrics.log
def log_metrics(ip_address, filename, file_size, user_agent, os_info, device_info):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(METRICS_LOG_FILE, 'a') as f:
        f.write(f'{timestamp} - IP: {ip_address}, User-Agent: {user_agent}, OS: {os_info}, Device: {device_info}, Uploaded File: {filename}, File Size: {file_size} bytes\n')

@app.route('/')
def index():
    logging.info('Rendering index.html')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received form data:", request.form)
    logging.info('Received file upload request')
    if 'file' not in request.files:
        logging.error('No file part in the request')
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        logging.error('No file selected')
        return jsonify({'error': 'No selected file'})

    if file:
        direction = request.form['direction']
        logging.info(f'Direction from HTML: {direction}')
        filename_without_extension = strip_extension(secure_filename(file.filename))
        timestamp = int(time.time())
        filename_with_timestamp = f"{filename_without_extension}_{timestamp}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp)
        logging.info(f'Saving file to: {file_path}')
        try:
            file.save(file_path)
            logging.info('File saved successfully')
            output = call_viewer(filename_with_timestamp, rankdir=direction)
            #Logging
            user_agent_string = request.headers.get('User-Agent')
            file_size = os.path.getsize(file_path)
            user_agent = request.headers.get('User-Agent')
            os_info, device_info = parse_user_agent(user_agent_string)
            log_metrics(request.remote_addr, filename_with_timestamp, file_size, user_agent, os_info, device_info)
            logging.info('File processed successfully')
            return jsonify({'success': 'File uploaded and processed successfully',
                            'download_png': output["png_download"],
                            'download_html': output["html_download"],
                            'download_json': output["json_download"],
                            'download_magjac': output['magjac_download']})
            
        except Exception as e:
            logging.error(f'Error saving or processing file: {str(e)}')
            return jsonify({'error': 'Error saving or processing file'})

@app.route('/downloads/<filename>')
def download_file(filename):
    logging.info(f'Download request for file: {filename}')
    generated_file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(generated_file_path):
        if filename.endswith('.html'):
            logging.info('Returning HTML file')
            return send_file(generated_file_path, as_attachment=False)
        else:
            logging.info('Returning other file')
            return send_file(generated_file_path, as_attachment=True)
    else:
        logging.error('File not found')
        return jsonify({'error': 'File not found'})

if __name__ == "__main__":
    app.run(debug=True)
