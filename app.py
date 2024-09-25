import os
from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

# Get the Downloads directory of the laptop
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

def download_youtube_playlist(playlist_url):
    # Fetch playlist information to get the title
    with yt_dlp.YoutubeDL() as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        playlist_title = playlist_info.get('title', 'Playlist')

    # Create a folder named after the playlist inside the Downloads directory
    playlist_folder = os.path.join(downloads_path, playlist_title)
    os.makedirs(playlist_folder, exist_ok=True)

    # yt-dlp options for download
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(playlist_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        'noplaylist': False  # Ensure downloading the entire playlist
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

    return playlist_folder

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        try:
            folder = download_youtube_playlist(playlist_url)
            return f"Playlist downloaded successfully! Check the folder: {folder}"
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
