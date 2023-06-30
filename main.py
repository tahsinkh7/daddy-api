from flask import Flask, request, make_response
from urllib.parse import urlparse, urlunparse
import requests
import re

app = Flask(__name__)
headers = {"Referer": "https://ntuplay.xyz/"}

def get_base_url(url):
    parsed_url = urlparse(url)
    base_path = '/'.join(parsed_url.path.split('/')[:-1]) + '/'
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, base_path, '', '', ''))
    return base_url

@app.route("/")
def credit():
    return "(Daddy-API) Made With ❤️ — By Tahsin Ahmed Dipto"

@app.route("/daddy-stream/<string:channel_id>.m3u8")
def handle_daddy-stream(channel_id):
    
    source_code = requests.get(f"https://daddylivehd.sx/embed/stream-{channel_id}.php").text 
    regex = r"source:\s*['\"](.*?)['\"]"
    match = re.search(regex, source_code)

    if match and match.group(1):
        url = match.group(1)
    response = requests.get(url, headers=headers)
    response_lines = response.text.splitlines()
    for index, line in enumerate(response_lines):
        if ".m3u8" in line:
            response_lines[index] = "/m3u8?id=" + line + f"&base={get_base_url(url)}"

    response = make_response("\n".join(response_lines))
    response.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    return response

@app.route("/m3u8")
def handle_m3u8():
    ts_id = request.args["id"]
    base = request.args["base"]
    response = requests.get(base + m3u8_id, headers=headers)
    myresponse = make_response(response.content)
    myresponse.headers["Content-Type"] = "video/mp2t"
    return myresponse

if __name__ == "__main__":
    app.run(debug=True)
