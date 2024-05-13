import os
import time

DOWNLOADS_FOLDER = '../downloads'
UPLOADS_FOLDER = '../uploads'
EXPIRY_DURATION = 1 * 3600  # 24 hours in seconds

def cleanup_folder(folder):
    current_time = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        # Get the modification time of the file
        modification_time = os.path.getmtime(file_path)
        # Calculate the expiry time
        expiry_time = modification_time + EXPIRY_DURATION
        # Check if the current time exceeds the expiry time
        if current_time > expiry_time:
            # If expired, delete the file
            os.remove(file_path)

def cleanup_downloads_folder():
    cleanup_folder(DOWNLOADS_FOLDER)

def cleanup_uploads_folder():
    cleanup_folder(UPLOADS_FOLDER)

if __name__ == "__main__":
    deleted_downloads = cleanup_downloads_folder()
    deleted_uploads = cleanup_uploads_folder()
    
     # Log deleted files
    # with open('/path/to/log/file_cleanup.log', 'a') as log_file:
    #     log_file.write(f'{datetime.datetime.now()} - Deleted files in uploads folder: {deleted_uploads}\n')
    #     log_file.write(f'{datetime.datetime.now()} - Deleted files in downloads folder: {deleted_downloads}\n')
