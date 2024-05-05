# import required libraries

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from functions import write_email, router, code_generator

# load dotenv
load_dotenv(find_dotenv())

# set environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]
# initialize flask app
app = App(token=SLACK_BOT_TOKEN)

# initialize flask app

flask_app = Flask('__name__')
handler = SlackRequestHandler(app)

def get_bot_user_id():
    """
    this method is used to generate the bot id
    to be used as an environment variable
    Returns:
        bot_id (str): bot user id
    """

    try:
        # initialize the slack client
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

def my_function(text):
    """
    this function is used to implement the assistant's actions
    Inputs:
        text (str): query that bot is supposes to answer
    Returns:
        response (str): the answer from the chatbot
    """

    response = code_generator(text)
    return response

@app.event("app_mention")
def handle_mentions(body, say):
    """
    this method is an event listener
    that is invoked whenever the bot is mentioned on slack
    Inputs:
        body (str): the event data dictionary returned by slack API
        say (callable): a function for sending a response to the channel
    """
    text = body["event"]["text"]
   
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention,"").strip()   #remove the bot id from the message
    say("Sure I will help you with that!")
    response = my_function(text)
    say(response)

@flask_app.route("/slack/events", methods = ["POST"])
def slack_events():
    """
    route for handling slack events
    the funciton passes the incoming HTTP request
    to the SlackRequestHandler for processing.
    Returns:
        Response: the HTTP response for handling a request
    """

    return handler.handle(request)

if __name__ == "__main__":
    # print(f"user_id: {get_bot_user_id()}")
    flask_app.run(debug=True, port=5001)


