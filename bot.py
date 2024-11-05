import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Drive API
def init_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = 'path/to/lofty-feat-440820-g9-1fddb464a839.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

drive_service = init_drive_service()

# Define the /start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a file and I'll upload it to Google Drive.")

# Handle files sent to the bot
def upload_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document

    if file:
        file_path = file.file_id + "_" + file.file_name
        file.download(file_path)

        # Upload to Google Drive
        file_metadata = {'name': file.file_name}
        media = MediaFileUpload(file_path, resumable=True)
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        update.message.reply_text("File uploaded to Google Drive successfully.")
        os.remove(file_path)  # Remove the file after upload

# Main function to set up the bot
def main():
    # Telegram Bot Token
    TOKEN = os.getenv("5367609170:AAF64lPgKDHu0uG_jOvkKqMp1xTiqt-aYNc")
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, upload_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
