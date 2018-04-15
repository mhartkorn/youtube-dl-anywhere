#!/usr/bin/env python3

from bottle import redirect, request, abort, Bottle

import youtube_dl

DEBUG_HOST = '0.0.0.0'
DEBUG_PORT = 5000
DEFAULT_FORMAT = '(mp4,webm)[height<=720]'

app = application = Bottle()


@app.route('/v/<raw_url:path>')
def raw(raw_url: str):
    url = combine_url_query(raw_url, request.query.decode())

    return find_url(DEFAULT_FORMAT, url)


@app.route('/f/<fmt>/<raw_url:path>')
def with_format(fmt: str, raw_url: str):
    url = combine_url_query(raw_url, request.query.decode())

    return find_url(fmt, url)


@app.route('/')
def index():
    return ""


@app.error(500)
def server_error(error):
    return "An internal error has occurred."


@app.error(404)
def server_error(error):
    return "Not found: {}".format(error)


def find_url(fmt: str, url: str):
    # Parameters for the youtube_dl module
    ydl_params = {
        'format': fmt,
        'cachedir': False,
        'logger': None,
        'noplaylist': True,
    }

    # Add http protocol if none is given for website
    if not url.startswith("http"):
        url = "http://{}".format(url)

    with youtube_dl.YoutubeDL(ydl_params) as ytdl:
        # Extract info
        result = ytdl.extract_info(url, download=False, process=False)

        formats = result.get('formats')

        if formats is None:
            return abort(404, "No such video")

        # Currently a hack because the given format doesn't seem to work properly
        filtered_fmt = [f for f in formats if f.get('ext') in ['mp4', 'webm'] and f.get('height', 9000) <= 720]

        if len(filtered_fmt) == 0:
            return abort(404, 'No format conforming "{}" found.'.format(DEFAULT_FORMAT))

        # Sort to get format with highest (vertical) resolution
        sorted(filtered_fmt, key=lambda f: f['height'])

        return redirect(filtered_fmt[0]['url'], code=301)


def combine_url_query(url, args):
    query_string = "?"

    for k, v in args.items():
        query_string += k + "=" + v

    return url + query_string


def main():
    app.run(host=DEBUG_HOST, port=DEBUG_PORT)


if __name__ == '__main__':
    main()
