from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
THUMBNAILS = {}

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# def error(update, context):
#     logger.warning(f"Update {update} caused error {context.error}")
#     context.bot.send_message(chat_id=update.message.chat_id, text="An error occurred while processing your request.")

def error(update, context):
    logger.warning(f"Update {update} caused error {context.error}")
    chat_id = update.message.chat_id if update.message else update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="An error occurred while processing your request.")


def set_thumbnail(update, context):
    try:
        video_message = update.message.reply_to_message.video
        thumbnail_photo = update.message.reply_to_message.photo[0]

        THUMBNAILS[video_message.file_id] = thumbnail_photo.file_id

        update.message.reply_text("Thumbnail set successfully!")
    except AttributeError:
        update.message.reply_text("Please reply to a video message to set the thumbnail.")

def view_thumbnail(update, context):
    try:
        video_message = update.message.reply_to_message.video
        if video_message.file_id in THUMBNAILS:
            thumbnail_id = THUMBNAILS[video_message.file_id]
            context.bot.send_photo(update.message.chat_id, photo=thumbnail_id)
        else:
            update.message.reply_text("No custom thumbnail set for this video.")
    except AttributeError:
        update.message.reply_text("Please reply to a video message to view the thumbnail.")

def delete_thumbnail(update, context):
    try:
        video_message = update.message.reply_to_message.video
        if video_message.file_id in THUMBNAILS:
            del THUMBNAILS[video_message.file_id]
            update.message.reply_text("Custom thumbnail deleted successfully!")
        else:
            update.message.reply_text("No custom thumbnail set for this video.")
    except AttributeError:
        update.message.reply_text("Please reply to a video message to delete the thumbnail.")

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("setthumb", set_thumbnail))
    dp.add_handler(CommandHandler("viewthumb", view_thumbnail))
    dp.add_handler(CommandHandler("deletethumb", delete_thumbnail))

    # Add an error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
