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
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    token = config._sections['bot_keys']['tipbot']
    sc = SlackClient(token)

    # print sc.api_call("chat.postMessage", channel="#bottesting",
    #                   text="You've been tipped!",
    #                   username='tipbot', icon_emoji=':doge:')

def main():
    slack()

if __name__ == "__main__":
    main()
