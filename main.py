import boto3
import pyrebase.pyrebase
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

from data.StorageFileDao import StorageFileDao
from domain.repository.DataBridgeRepository import DataBridgeRepository
from util.FileUtils import get_firebase_config, get_s3_config, get_bot_config, clear_photo


def start(update: Update, context):
    user = {
        'id': update.message.from_user.id,
        'name': update.message.from_user.username,
    }

    data = DataBridgeRepository.get_instance().get_user(user)

    if DataBridgeRepository.get_instance().is_user_exists(data):
        DataBridgeRepository.get_instance().create_new_profile(user)
        update.message.reply_text('Привет, новый пользователь, введи этот код в приложение на своём компьютере: ' + str(user['id']))
    else:
        update.message.reply_text('Вы уже зарегистрированы, код для поключения с компьютера: ' + str(user['id']))

def handle_photo(update: Update, context: CallbackContext):
    user = {
        'id': update.message.from_user.id,
        'name': update.message.from_user.username,
    }

    data = DataBridgeRepository.get_instance().get_user(user)

    if DataBridgeRepository.get_instance().is_user_exists(data):
        update.message.reply_text('Вы не зарегестрированы, напишите /start и отправьте картинку ещё раз')
    else:
        item = update.message.photo[-1]
        file_name = context.bot.get_file(item.file_id).download()
        DataBridgeRepository.get_instance().save_file(file_name, user)
        clear_photo(file_name)
        update.message.reply_text('Картинка сохранена')

        DataBridgeRepository.get_instance().create_new_profile(user, file_name)

        update.message.reply_text('Картинка сохранена')



def main():
    s3_config = get_s3_config()
    firebase_config = get_firebase_config()
    bot_config = get_bot_config()

    firebase = pyrebase.initialize_app(firebase_config)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_config['aws_access_key_id'],
        aws_secret_access_key=s3_config['aws_secret_access_key'],
        region_name=s3_config['region_name'],
        endpoint_url=s3_config['endpoint_url'],
    )

    DataBridgeRepository.initialize(
        firebase=firebase,
        s3_client=s3_client,
        s3_main_bucket=bot_config['bucket_name']
    )

    token = bot_config['token']
    updater = Updater(token)

    dispatcher = updater.dispatcher
    photo_handler = MessageHandler(Filters.photo, handle_photo, run_async=True)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(photo_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
