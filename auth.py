

import os
from slackclient import SlackClient
import pytz
import datetime

CLIENT_ID = os.environ.get('CLIENT_ID') 
CLIENT_SECRET = os.environ.get('CLIENT_SECRET') 
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN') 

#authed_teams = {}

timezones = []
t = list(filter(lambda x: 'Asia' in x, pytz.all_timezones))
for zone in t:
    info = {
        "text": zone,
        "value": zone,
    }
    timezones.append(info)

# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "What is your timezone?",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "timezone_options",
        "actions": [
            {
                "name": "timezone_list",
                "text": "Select your timezone.",
                "type": "select",
                "options": timezones
            }
        ]
    }
]

class Bot(object):
	""" Instanciates a Bot object to handle Slack onboarding interactions."""

	def __init__(self):
	    super(Bot, self).__init__()
	    self.name = "hello_bot"
	    self.emoji = ":robot_face:"
	    # When we instantiate a new bot object, we can access the app
	    # credentials we set earlier in our local development environment.
	    self.oauth = {"client_id": CLIENT_ID,
	                  "client_secret": CLIENT_SECRET,
	                  # Scopes provide and limit permissions to what our app
	                  # can access. It's important to use the most restricted
	                  # scope that your app will need.
	                  "scope": "bot"}
	    self.verification = VERIFICATION_TOKEN
	    self.client = SlackClient("")
	    # We'll use this dictionary to store the state of each message object.
	    # In a production envrionment you'll likely want to store this more
	    # persistantly in  a database.
	    self.messages = {}

	def auth(self, code):
		"""Authenticate with OAuth and assign correct scopes.
		"""
		auth_response = self.client.api_call(
							"oauth.access",
							client_id=self.oauth["client_id"],
							client_secret=self.oauth["client_secret"],
							code=code)
		team_id = auth_response["team_id"]
		# authed_teams[team_id] = {"bot_token":
		#                          auth_response["bot"]["bot_access_token"]}
		bot_token = auth_response["bot"]["bot_access_token"]
	
		self.client = SlackClient(bot_token)
		self.message("What is your timezone, please?",attachments_json)
	   

	def message(self, text, attachments):
		"""send message to slack"""
		self.client.api_call(
	                  "chat.postMessage",
	                  channel="#general",
	                  text=text,
	                  attachments=attachments
	                    )


        