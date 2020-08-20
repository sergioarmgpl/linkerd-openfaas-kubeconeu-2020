import socket
import requests
import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
#from onboarding_tutorial import OnboardingTutorial

app = Flask(__name__)
#basic information signing secret
slack_events_adapter = SlackEventAdapter("3e27", "/slack/events", app)
#oauth and permissions
slack_web_client = WebClient(token="xoxb-872466")
host = socket.gethostname()


@slack_events_adapter.on("team_join")
def onboarding_message(payload):
    event = payload.get("event", {})
    user_id = event.get("user", {}).get("id")
    response = slack_web_client.im_open(user_id)
    channel = response["channel"]["id"]
    slack_web_client.chat_postMessage(channel=channel,text=host+": :thinking_face:")

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    event = payload.get("event", {})
    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")
    slack_web_client.chat_postMessage(channel=channel_id,text=host+": :face_with_rolling_eyes:")

@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
#    ts = event.get("ts")
    ts = ""
    if text != None and user_id != "UV84PJNSC":
        print("New message: "+text+" user: "+user_id) 
        if text == "kubeconeu":
            slack_web_client.chat_postMessage(channel=channel_id,text=host+": Is so cool :smiley:",thread_ts=ts)
            requests.get("http://microservice")
        else:
            slack_web_client.chat_postMessage(channel=channel_id,text=host+": i dont now that conference :smiley:",thread_ts=ts)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(host='0.0.0.0',port=5000, debug=True)
#    app.run(host='0.0.0.0',port=443,ssl_context=('/etc/letsencrypt/live/bot.curzona.net/fullchain.pem', '/etc/letsencrypt/live/bot.curzona.net/privkey.pem'))
