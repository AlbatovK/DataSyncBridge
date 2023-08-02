import time
from threading import Thread
import os as oss
import boto3
from boto3.s3.transfer import TransferConfig

from telegram import message, InputMediaPhoto, ReplyKeyboardMarkup, File, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

token = '5573009501:AAGogcHnl1zvrQiI3BCQTkl1egypD_ujwJc'
BUCKET_NAME = 'akkarinbaket'
config = TransferConfig(use_threads=False)
os = boto3.client(
    's3',
    aws_access_key_id='YCAJEoT3R9zc1V66Fmgex549R',
    aws_secret_access_key='YCMPLZiTXMP6-dwc-Vy2XzIISpWls8Lb_gvf9uNH',
    region_name='ru-central1',
    endpoint_url='https://storage.yandexcloud.net',
)


def ls():
    for bucket in os.list_buckets()['Buckets']:
        print(bucket['Name'])


def keys(bucket_name):
    for key in os.list_objects(Bucket=bucket_name)['Contents']:
        print(key['Key'])


def upload(bucket_name, object_name1, object_name2):
    os.upload_file(object_name1, bucket_name, object_name2, Config=config)

'''
cnfg = {
    'apiKey': "AIzaSyDdvqyuUeW6-lBt0gEFb9tHxiNh9Ty2Hlc",
    'authDomain': "sassharesigma.firebaseapp.com",
    'databaseURL': "https://sassharesigma-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "sassharesigma",
    'storageBucket': "sassharesigma.appspot.com",
    'messagingSenderId': "447709495445",
    'appId': "1:447709495445:web:38a3f28766998de794db9c"
}

import pyrebase

firebase = pyrebase.pyrebase.initialize_app(cnfg)

firebase.database().child('подвал').child('Артеми').set({'name':'idk', 'sex':'gay'})
def download(bucket_name, object_name):
    os.download_file(bucket_name, object_name, object_name, Config=config)
    
'''




# upload(BUCKET_NAME, 'C:/Users/user/Desktop/test.jpg')
# download(BUCKET_NAME, 'test.jpg')


def save(update: Update, context: CallbackContext):
    test = update.message.photo[-1]

    a = context.bot.get_file(test).download()
    upload(BUCKET_NAME, "C:/Users/user/PycharmProjects/Share/" + a, a)
    #oss.remove(a)

    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=test)


def main():
    # upload(BUCKET_NAME, "C:/Users/user/PycharmProjects/Share/" + 'test.jpg', 'test')

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.photo, save))

    updater.start_polling()


if __name__ == '__main__':
    main()


