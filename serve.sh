#!/bin/sh

PORT=${1-8000}

# pull in 3rd party libraries from cdn.jsdelivr.net
./fetch_resources.sh

# host local webserver and specify the index.html file to serve
python3 -m http.server --bind 127.0.0.1 "$PORT"
