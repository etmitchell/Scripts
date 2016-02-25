# This is a slackbot to let you know when the International
# Space Station is overhead. Right now we're hardcoded for
# The Boston/Greater Boston area, but in the future it would
# be neat to get your location based off IP/etc.

import urllib2
import json
from slackclient import SlackClient
import time
from collections import defaultdict
import ConfigParser
import os

BOSTON = (42.3601, 71.0589)
# 1 degree of latiude at 45N/S is ~78.71 km.
# (source: https://en.wikipedia.org/wiki/Decimal_degrees)
# That should be plenty to allow for people in the
# Greater Boston Area to know when the ISS is overhead.

def get_coords():
    static_loc = BOSTON
    iss_loc = defaultdict(float)
    iss_endpoint = "http://api.open-notify.org/iss-now.json"

    req = urllib2.Request(iss_endpoint)
    reply = urllib2.urlopen(req)
    iss_loc = json.loads(reply.read())

    if iss_loc['message'] == 'success':
        iss_loc['lat'] = iss_loc['iss_position']['latitude']
        iss_loc['long'] = iss_loc['iss_position']['longitude']
        return iss_loc
    else:
        return None

def slack(lat=None,lng=None):
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    token = config._sections['bot_keys']['spacebot']
    sc = SlackClient(token)
    # Currently printing for debugging
    print sc.api_call("api.test")
    print sc.api_call("channels.info", channel="1234567890")
    print sc.api_call("chat.postMessage", channel="#insertyourchannelhere",
                      text="The International Space Station is over boston! :tada:",
                      username='spacebot', icon_emoji=':crescent_moon:')

def main():
    response = get_coords()

    lat = response['lat']
    lng = response['long']

    if lat - 0.5 <= BOSTON[0] <= lat + 0.5:
        print "On the same latitude!"
        if lng - 0.5 <= BOSTON[1] <= lat + 0.5:
            print "On the same longitude!"
            print "OVERHEAD!"
            slack(lat,lng)
    else:
        print "Currently at: ({0},{1})".format(lat,lng)

if __name__ == "__main__":
    # execute only if run as a script
    while True:
        main()
        time.sleep(5)
