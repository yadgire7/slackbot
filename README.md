# slackbot
A conversational AI Slack chatbot


## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/yadgire7/slackbot.git
```

2. Navigate to the cloned repository directory:

```
cd slackbot
```

3. Install the required dependencies by executing the following command:

```
pip install -r requirements.txt
```

4. Create a .env file in the directory or create environment variables on your system.

For .env file:
```
<environment_variable_name>="<your_key>"
```

For Linux/ Mac OS: 
```
export <environment_variable_name>=<your_key>
```
For Windows OS:
- Seach 'env' in the search panel
- Click 'Edit the system environment variables'
- Click 'Environment variables'
- Click 'New' under the 'System Variables' section
- Add your system variables

5. Get your secret tokens
- Go to 'OAuth & Permissions' tab in the menu bar on the left side of api.slack.com/apps after to login to your Workspace.
- Copy the 'Bot User OAuth Token' and assign it to 'SLACK_BOT_TOKEN'
- Go to 'Basic Information' tab in the menu bar on the left side of api.slack.com/apps
- Copy the 'Signing Secret' token under the App Credentials section and assign it to 'SLACK_SIGNING_SECRET'
- Print response["user_id"] in the get_bot_user_id method in app.py to get 'SLACK_BOT_USER_ID'
- If you want to use OpenAI models, get your OPENAI_API_KEY from https://openai.com/index/openai-api

6. Run you flask app

```
python app.py
```

7. Host your flask app using ngrok
- install ngrok
- assign the port for your temporary server
```
ngrok http <port number of you flask app>
```
- Copy the generated ngrok server link 
- Go to 'Event Subscriptions' tab in the menu bar on the left side of api.slack.com/apps
- Paste the url in the 'Request URL' section and append '/slack/events' to the URL and click 'Save Changes' button
- Go to 'Event Subscriptions' tab in the menu bar and click 'Reinstall to Workspace' button

8. Use the Slack Bot
- Add your bot to the Workspace
- Type the query after mentioning the bot.

