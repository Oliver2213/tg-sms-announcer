# tg-sms-announcer

Bridges messages sent to a telegram channel to a list of phone numbers (via sms using Twilio).

## Setup
* Clone or fork this repository
* Copy .env.example to .env and fill in the values.
* Create a virtual environment and install the packages used:
```
python -m venv .virtualenv
pip install -r requirements.txt
```
* Then run (or automate, dockerize, etc) python announcer.py after activating the virtual environment in .virtualenv.

## Use as a bot vs. through your personal account
Using a bot is recommended over your personal account, though either choice is fine. Bots have the advantage that if you ever leave the channel, this script won't stop functioning. Muting a channel may also silence messages (haven't tested), so using one ensures your changes don't affect the announcer.
If the variable 'TELEGRAM_BOT_TOKEN' is set in either the environment or a .env file, the announcer will act as a bot. Otherwise, it will log in as whatever account belongs to the API ID and hash you provide it.

## Required credentials
You will need a telegram and twilio account and their associated API and usage tokens.
For twilio, you will likely also need a phone number to send the messages from (if sending to numbers that are not your own).

## Adding a bot to a channel
If you are running this as a bot, you will need to add it to whatever channels or chats you wish it to announce from. You may do this either:
* Through a telegram app (such as the desktop, web or mobile ones), or
* by manually doing it in a rep with this library.

I will likely add a command to do this at some point in the future, but for now here's how you can do it manually (for example if the clients don't work, as was in my case):
Open a python shell using asyncio and import what we'll need:
```
python -m asyncio
from telethon import TelegramClient
# Log into the API as your personal account, which has admin rights to the chat or channel you wish to add the bot to.
# If you already have your API id and hash in a .env file, uncomment the lines below.
# Otherwise, set 'tg_api_id' and 'tg_api_hash' manually
#from dotenv import dotenv_values
#config = dotenv_values(".env")
#tg_api_id, tg_api_hash = config['TELEGRAM_API_ID'], config['TELEGRAM_API_HASH']
client = TelegramClient('personal_tg', tg_api_id, tg_api_hash)
cl.start() # connect and authenticate; should ask for phone number
# Get the channel / chat and bot you want to use.
# This could be through client.get_dialogs(), client.get_entity, etc.
# See telethon's docs for more on enteties.
# Set channel and bot variables, then
# Consider limiting the admin rights your bot has to only what it will use.
result = await client.edit_admin(channel, bot, is_admin=True)
await client.logout() # Log out and delete the session file.
```
