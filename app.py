from flask import Flask, render_template_string, request
import requests
import re

app = Flask(__name__)

# Function to fetch page source
def fetch_page_source(url):
    referer = "https://live.reddit-soccerstreamss.online/"
    headers = {
        'Connection': 'keep-alive',
        'Origin': 'https://live.reddit-soccerstreamss.online/',
        'Referer': referer,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page source: {e}")
        return None

@app.route('/')
def index():
    # Fetching query parameters (id and id2)
    id = request.args.get('id', 'defaultID')
    id2 = request.args.get('id2', '1111')

    # URL to fetch the page source from
    target_url = f"https://live.reddit-soccerstreamss.online/reddit/{id}.php"
    page_source = fetch_page_source(target_url)

    if page_source:
        # Match the new player.load structure and extract the source URL
        match = re.search(r"player\.load\(\{source: '([^']+)'", page_source)
        if match:
            hls_url = match.group(1)
            return render_template_string('''
                <html>
                <head>
                    <title>Video Player</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            height: 100vh;
                            background-color: #f4f4f4;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            overflow: hidden;
                        }
                        #player-container {
                            width: 80%;
                            height: 80%;
                            background-color: #000;
                            border-radius: 10px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                        }
                        iframe {
                            width: 100%;
                            height: 100%;
                            border: none;
                            border-radius: 10px;
                        }
                    </style>
                </head>
                <body>
                    <div id="player-container">
                        <iframe src="https://anym3u8player.com/tv/video-player.php?url={{ hls_url }}" width="100%" height="100%" frameborder="0" allowfullscreen></iframe>
                    </div>
                </body>
                </html>
            ''', hls_url=hls_url)
        else:
            return "Failed to extract the HLS URL from player.load."
    else:
        return "Failed to fetch the page source."

if __name__ == '__main__':
    app.run(debug=True)
