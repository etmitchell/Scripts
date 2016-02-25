# TIP BOT!
# Slack Bux/Slack Bucks

import urllib2
import json
from slackclient import SlackClient
import time
from collections import defaultdict

def slack(lat=None,lng=None):
    token = "get your own"
    sc = SlackClient(token)
    print sc.api_call("api.test")
    print sc.api_call("chat.postMessage", channel="#bottesting",
                      text="You've been tipped!",
                      username='tipbot', icon_emoji=':doge:')

def main():
    slack()

if __name__ == "__main__":
    # while True:
    main()
