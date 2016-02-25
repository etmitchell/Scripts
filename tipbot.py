# TIP BOT!
# Slack Bux/Slack Bucks

import urllib2
import json
from slackclient import SlackClient
import time
from collections import defaultdict
import ConfigParser
import os

def slack():
    pass

def send_message(sc,keyword=None):
    sc.api_call("chat.postMessage", channel="#bottesting",
                      text= "DID SOMEONE SAY {0}?!?".format(keyword),
                      username='tipbot', icon_emoji=':doge:')

def main():
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    token = config._sections['bot_keys']['testing']
    sc = SlackClient(token)

    if sc.rtm_connect():
        while True:
            print sc.rtm_read()
            new_evts = sc.rtm_read()
            for evt in new_evts:
                print(evt)
                if "type" in evt and evt["type"] == "message":
                    if "text" in evt and "tipbot:" in evt["text"]:
                        keyword = evt["text"].rsplit(':', 1)[1].encode('utf8')
                        send_message(sc,keyword)

            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            print(evt)
            if "type" in evt:
                if evt["type"] == "message" and "text" in evt:
                    message=evt["text"]
        time.sleep(1)

if __name__ == "__main__":
    main()
