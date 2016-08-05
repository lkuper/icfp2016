#!/usr/bin/env python3

## Requires pycurl. Downloads problems.

import json
import pycurl
import time
from io import BytesIO

APIKEY = None

## First, get the list of snapshots. Then find the latest snapshot.

def load_api_key():
    out = None
    with open("APIKEY") as infile:
        lines = infile.readlines()
        out = lines[0].strip()
    return out

URLPREFIX = "http://2016sv.icfpcontest.org/api/"
def get_curl(apicall):
    """Build a Curl with all the common options set."""
    c = pycurl.Curl()
    c.setopt(pycurl.ENCODING, 'gzip,deflate')
    c.setopt(pycurl.FOLLOWLOCATION, True)
    headers = ["Expect:", "X-API-Key: " + APIKEY]
    c.setopt(pycurl.HTTPHEADER, headers)

    c.setopt(pycurl.URL, URLPREFIX + apicall)
    return c

def get_json_response(c):
    """Do the HTTP call, turn the returned json into a dict, and return it.
    
    Also sleep for a second, so we don't go over the rate limit."""
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    time.sleep(1)
    return json.loads(body.decode("utf-8"))

# 'http://2016sv.icfpcontest.org/api/snapshot/list'
def download_snapshots():
    c = get_curl("snapshot/list")
    d = get_json_response(c)
    return d

def main():
    global APIKEY
    APIKEY = load_api_key()
    print("loaded API key:", APIKEY)

    download_snapshots()

if __name__ == "__main__": main()
