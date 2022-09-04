# tg-sms-announcer: sends messages from a telegram channel to a specified list of phone numbers using sms.
# Required Telegram and Twilio credentials and a twilio phone number.

import os
import asyncio
from telethon import TelegramClient, events
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv() 

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


# Telegram API and app credentials.
tg_api_id = os.getenv("TELEGRAM_API_ID", "")
tg_api_hash = os.getenv("TELEGRAM_API_HASH", "")
tg_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
# Where do we store creds? Default to tg-sms-announcer.
# CHANGE IF USING MULTIPLE SCRIPT INSTANCES WITH MULTIPLE ACCOUNTS FROM THE SAME DIRECTORY!
tg_session_filename = os.getenv("TELEGRAM_SESSION_FILENAME", "tg-sms-announcer")

# Twilio Credentials
tw_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
tw_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
tg_client = TelegramClient(tg_session_filename, tg_api_id, tg_api_hash)
#tg_client.start(bot_token=tg_bot_token)
# tw_client = Client(tw_account_sid, tw_auth_token)

async def main():
  print("Starting main...")
  await tg_client.start(bot_token=tg_bot_token)
  print("Started. Getting me...")
  me = await tg_client.get_me()
  print(f"Logged in as @{me.username}")
  await tg_client.run_until_disconnected()

@tg_client.on(events.NewMessage(incoming=True))
async def handler(event):
  print(f"Received message from {event.message.post_author}: {event.message.message}.")

asyncio.run(main())
