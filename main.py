#!/usr/bin/python

import bluetooth
import time
import urllib, urllib2
import os, json

def find(id):
        result = bluetooth.lookup_name(id, timeout=4)
        if result == None:
            return "OUT"
        else:
            return "IN"

def get_devices(opts):
    headers = {"Authorization": "Bearer {0}".format(opts["token"])}
    data = urllib.urlencode({})
    req = urllib2.Request(opts["url"], data, headers)
    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        print e.code
        return []

def load_opts():
    token = os.getenv("SERVICE_TOKEN", "willnotwork")
    url = os.getenv("SERVICE_URL", "http://127.0.0.1:3000/")
    
    return {"token": token, "url": url}

def send_status(opts, id, status):
    url = "{0}{1}/{2}".format(opts["url"], id, status) 
    print url
    headers = {"Authorization": "Bearer {0}".format(opts["token"])}
    data = urllib.urlencode({})
    req = urllib2.Request(url, data, headers)
    try:
        urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e.code

if __name__ == "__main__":
    opts = load_opts()
    while True:
        try:
            devices = get_devices(opts)
            for d in devices:
                id = d["_id"]
                blueid = d["bluetoothId"]
                status = find(blueid)
                send_status(opts, id, status)
        except Exception as e:
            print "error: {0}".format(e)
        time.sleep(10)