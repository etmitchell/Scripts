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
<<<<<<< HEAD
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    token = config._sections['bot_keys']['tipbot']
    sc = SlackClient(token)

    # print sc.api_call("chat.postMessage", channel="#bottesting",
    #                   text="You've been tipped!",
    #                   username='tipbot', icon_emoji=':doge:')
=======
    token = "get your own"
    sc = SlackClient(token)

    print sc.api_call("chat.postMessage", channel="#bottesting",
                      text="You've been tipped!",
                      username='tipbot', icon_emoji=':doge:')
>>>>>>> 06b033380b2da8a74ed625672633a8b7126d562d

def main():
    slack()

if __name__ == "__main__":
    main()
