# tg-sms-announcer: sends messages from a telegram channel to a specified list of phone numbers using sms.
# Required Telegram and Twilio credentials and a twilio phone number.

import os
import sys
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

# Twilio Credentials and numbers
tw_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
tw_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
tw_src_number = os.getenv("TWILIO_SRC_NUMBER")
# Temporary, will add more flexible way to specify several numbers
tw_dst_number = os.getenv("TWILIO_DST_NUMBER")

# If no Twilio source number is provided, quit with a message.
if not tw_src_number:
  print("Error: TWILIO_SRC_NUMBER' not set in either .env of as an environment variable. You must have a Twilio number to send sms messages from.", file=sys.stderr)
  quit(1)

# Create clients for Telegram and Twilio with our credentials
tg_client = TelegramClient(tg_session_filename, tg_api_id, tg_api_hash)
tw_client = Client(tw_account_sid, tw_auth_token)

#tw_client.http_client.logger.setLevel(logging.INFO)


async def main():
  print("Starting telegram to sms announcer...")
  if tg_bot_token:
    await tg_client.start(bot_token=tg_bot_token)
  else:
    await tg_client.start()
  print("Connected and logged in to Telegram.")
  me = await tg_client.get_me()
  print(f"Logged in as @{me.username}")
  await tg_client.run_until_disconnected()

@tg_client.on(events.NewMessage(incoming=True))
async def handler(event):
  print(f"Received message from {event.message.post_author}: {event.message.message}.")
  print(f"Forwarding to {tw_dst_number}...")
  tw_client.messages.create(to=tw_dst_number, from_=tw_src_number, body=event.message.message)

if __name__ == '__main__':
  asyncio.run(main())
