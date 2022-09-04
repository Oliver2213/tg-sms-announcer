# tg-sms-announcer: sends messages from a telegram channel to a specified list of phone numbers using sms.
# Required Telegram and Twilio credentials and a twilio phone number.

import os
import asyncio
from telethon import TelegramClient, events

# Telegram API and app credentials.
tg_api_id = os.getenv("TELEGRAM_API_ID", "")
tg_api_hash = os.getenv("TELEGRAM_API_HASH", "")
# Where do we store creds? Default to tg-sms-announcer.
# CHANGE IF USING MULTIPLE SCRIPT INSTANCES WITH MULTIPLE ACCOUNTS FROM THE SAME DIRECTORY!
tg_session_filename = os.getenv("TELEGRAM_SESSION_FILENAME", "tg-sms-announcer")

async def main():
  client = TelegramClient(tg_session_filename, tg_api_id, tg_api_hash)
  await client.start()

asyncio.run(main())
