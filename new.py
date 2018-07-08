from flask import Flask, request, make_response, Response, render_template
import os
import json
import pytz
import datetime
import time
import re
import auth
import gevent #workers-timeout
from slackclient import SlackClient

#SLACK_WEBHOOK_SECRET ="9OXQcUS9PqzdAvyh7E6KWqP6"
DELAY = 1 #86400 #24 hours
starterbot_id = None # starterbot's user ID in Slack: value is assigned after the bot starts up

pyBot = auth.Bot()
slack_client = pyBot.client

app = Flask(__name__)

#The endpoint Slack will load your menu options from
@app.route("/options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    # Dictionary of menu options which will be sent as JSON
    menu_options = {"options": timezones}
    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')


@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id   = pyBot.oauth["client_id"]
    scope       = pyBot.oauth["scope"]
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    """"""
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    
    #print(code_arg)
    pyBot.auth(code_arg)                  
    return make_response("Thank you! You have successfully installed the bot"), 200


# The endpoint Slack will send the user's menu selection to
@app.route("/slack", methods=["POST"])
def message_actions():
    """send "hi" at 12pm of the selected timezone"""
    #print(request)
    #print(request.form)
    form_json = json.loads(request.form["payload"])
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    intz = pytz.timezone(selection)
    nowdt = datetime.datetime.now(intz)
    nowt = nowdt.strftime('%H:%M:%S')
    midday=datetime.time(hour=11, minute=45,second=59,tzinfo=intz).strftime('%H:%M:%S')
    #midday=datetime.time(hour=11, minute=59,second=59,tzinfo=intz).strftime('%H:%M:%S')
    print(nowt)
    print(midday)
    while True:  
        print("out") 
        if(nowt==midday):
            print("in-not")
            while True:
                print("in")
                pyBot.message("hi", [])
                #time.sleep(30)
                gevent.sleep(30)
                print(nowt)
        #time.sleep(DELAY)
        gevent.sleep(DELAY)

    return make_response(""),200



# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host = '0.0.0.0', port=5000)