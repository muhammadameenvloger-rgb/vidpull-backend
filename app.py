from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "VidPull Backend is Running!"

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    quality = data.get("quality", "best")
    
    # Quality logic
    if quality == "best":
        fmt = "best"
    elif quality == "mp3":
        fmt = "bestaudio/best"
    else:
        fmt = f"bestvideo[height<={quality}]+bestaudio/best"

    ydl_opts = {
        'format': fmt,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Seedha download link nikalne ke liye
            download_url = info.get('url', None)
            return jsonify({"status": "ok", "download_url": download_url, "title": info.get('title')})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
