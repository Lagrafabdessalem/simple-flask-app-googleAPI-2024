
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = ""
SEARCH_ENGINE_ID = ""


@app.route('/')
def index():
    return render_template('index.html', results=None, error=None)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('searchType', '')
    file_type = request.args.get('fileType', '')

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
    }

    if search_type == 'image':
        params['searchType'] = 'image'
    elif search_type == 'fileType' and file_type:
        params['fileType'] = file_type

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        items = results.get("items", [])
        return render_template('index.html', results=items, error=None)
    except requests.RequestException as e:
        return render_template('index.html', results=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
