# Youtube-dl Everywhere

Youtube-dl Everywhere lets you play videos from popular websites on any device with a network-capable video player.
The only thing you need to run this application is a server with Python 3.

It uses [youtube-dl](https://github.com/rg3/youtube-dl) to find videos on popular websites and extract the HTTP URL
of the video. After that it leverages HTTP status code 301 to redirect to the original video source without needing
to stream the video by itself.

### Limitations

The used method doesn't allow playback of DASH based videos as the segment selection cannot be implemented in a
player-agnostic way. E.g. for YouTube the default format is unsupported, please use the explicit format selection
route to specify a format. In the future there might be a list of supported formats for specific websites.

Formats cannot contain full youtube-dl compatible strings as slashes ("/") are currently unsupported.

This project is Python 3 only. If you want Python 2 support, please submit a PR.
