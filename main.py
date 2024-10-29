import os
import re  # Added import
from flask import Flask, render_template, send_from_directory
import threading
import webbrowser
from tkinter import Tk, filedialog

app = Flask(__name__)

def select_video_directory():
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Video Directory")
    root.destroy()
    return directory

def natural_sort_key(s):
    """
    Splits the string into a list of integers and lowercase strings for natural sorting.
    E.g., "10 - Video.mp4" becomes [10, " - video.mp4"]
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('(\d+)', s)]

def get_video_files(directory):
    supported_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
    videos = [f for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]
    videos.sort(key=natural_sort_key)  # Apply natural sort
    return videos

@app.route('/')
def index():
    return render_template('index.html', videos=video_files)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(video_directory, filename)

def start_flask():
    # Bind to host '127.0.0.1' and port '8000'
    app.run(host='127.0.0.1', port=8000, debug=False)

if __name__ == "__main__":
    # Step 1: Select directory
    video_directory = select_video_directory()
    if not video_directory:
        print("No directory selected. Exiting.")
        exit()

    # Step 2: Get video files
    video_files = get_video_files(video_directory)
    if not video_files:
        print("No video files found in the selected directory. Exiting.")
        exit()

    # Step 3: Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Step 4: Open the web page in the default browser
    webbrowser.open("http://127.0.0.1:8000/")

    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down.")
        exit()
