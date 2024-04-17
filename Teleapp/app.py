from flask import Flask, redirect, request, jsonify
import string
from random import choices

app = Flask(__name__)

url_mapping = {}

def generate_short_identifier(length=6):
    allowed_chars = string.ascii_letters + string.digits
    return ''.join(choices(allowed_chars, k=length))

def shorten_url(url):
    for key, value in url_mapping.items():
        if value == url:
            return f"http://localhost:5000/{key}"
    short_id = generate_short_identifier()
    while short_id in url_mapping:
        short_id = generate_short_identifier()
    url_mapping[short_id] = url
    return f"http://localhost:5000/{short_id}"

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the URL Shortener! Use /shorten?url=YOUR_URL to shorten your URL."

@app.route('/shorten', methods=['GET'])
def api_shorten_url():
    original_url = request.args.get('url')
    if original_url:
        shortened_url = shorten_url(original_url)
        return jsonify({'original_url': original_url, 'shortened_url': shortened_url})
    else:
        return "Error: No URL provided. Please provide a URL as a query parameter."

@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    else:
        return "Error: URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
