import zlib
from flask import Flask, request, redirect


app = Flask(__name__)
short_urls_dict = {}



def shorten_long_url(long_url):
    short_str = hex(zlib.crc32(long_url.encode()) & 0xffffffff)
    short_str = short_str.split("0x")[1]
    return short_str


@app.route("/new-url", methods=["POST", "GET"])
def shorten_url():
    url_to_shorten = ""
    try:
        print(request.json)
        url_to_shorten = request.json.get("url")
        short_url = shorten_long_url(url_to_shorten)
        short_urls_dict[short_url] = url_to_shorten

    except:
        return "Invalid JSON"

    return request.root_url + short_url


@app.route("/<string:short_url>")
def handle_short_url(short_url):
    long_url = short_urls_dict.get(short_url, None)
    if(long_url):
        return redirect("https://" + long_url, code=301)
    else:
        return "Not Found"


@app.route("/")
def index_page():

    return "<p>Hello, World!</p>"
