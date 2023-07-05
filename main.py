from flask import Flask, request, make_response
from urllib.parse import urlparse, urlunparse
import requests
import re

app = Flask(__name__)
headers = {"Referer": "https://ntuplay.xyz/"}
headers2 = {"Referer": "https://millionscast.com/"}

def get_base_url(url):
    parsed_url = urlparse(url)
    base_path = '/'.join(parsed_url.path.split('/')[:-1]) + '/'
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, base_path, '', '', ''))
    return base_url

@app.route("/")
def credit():
    return "(Daddy-API) Made With ðŸ’— By Sabbiriptv"

@app.route("/api")
def handle_api(channel_id):
    
    source_code = requests.get(f"https://daddylivehd.sx/embed/stream-{channel_id}.php").text 
    regex = r"source:\s*['\"](.*?)['\"]"
    match = re.search(regex, source_code)

    if match and match.group(1):
        url = match.group(1)
    response = requests.get(url, headers=headers)
    response_lines = response.text.splitlines()
    for index, line in enumerate(response_lines):
        if ".ts" in line:
            response_lines[index] = "/ts?id=" + line + f"&base={get_base_url(url)}"

    response = make_response("\n".join(response_lines))
    response.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    return response

@app.route("/ts")
def handle_ts():
    ts_id = request.args["id"]
    base = request.args["base"]
    response = requests.get(base + ts_id, headers=headers)
    myresponse = make_response(response.content)
    myresponse.headers["Content-Type"] = "video/mp2t"
    return myresponse

# ----------------

@app.route("/api-v2")
def handle_api2(channel_id):
    
    response = requests.get(f"https://millionscast.com/crichdwas.php?player=desktop&live={channel_id}", headers={"Referer": "https://stream.crichd.vip/"})

    match_string = "return("
    if "return(" not in response.text:
        match_string = "return ("


    first_index = response.text.find(match_string) + len(match_string)
    last_index = response.text.find(".join")
    link_array = eval(response.text[first_index:last_index])
    joined = "".join(link_array)
    final_link = joined.replace("\/\/\/\/", "//").replace("\/", "/")
    response = requests.get(final_link, headers=headers2)
    response_lines = response.text.splitlines()
    for index, line in enumerate(response_lines):
        if ".ts" in line:
            response_lines[index] = "/ts-v2?id=" + line + "&base=" + get_base_url(final_link)
    myresponse = make_response("\n".join(response_lines))
    myresponse.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    return myresponse

@app.route("/ts-v2")
def handle_ts2():
    ts_id = request.args.get("id")
    base = request.args.get("base")
    final = base + ts_id
    response = requests.get(final)
    myresponse = make_response(response.content)
    myresponse.headers["Content-Type"] = "video/MP2T"
    return myresponse

if __name__ == "__main__":
    app.run(debug=True)
