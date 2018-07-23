# this is remastered TelegramBot api with threading module
import requests
import json
import apiai
import threading
from os import path
'''

    Use before running your bot, it has attributes:
    bot_set(telegramBotToken, (optional) dialogFlowToken, (optional) dialogFlowSession, (optional) dialogFlowLanguage)

    Then, your bot is ready.
    Methods:

        Information about your bot, returns a dictionary about with the information:
        info(author, bot_name, description)

        Creates and returns a json file with the information about your bot's chat
        get_info(j_create=True)  # if True => saves it on your computer as a file

        Sends a message
        msg_send(chat_id, text)

        Generates and returns a response, which is editable on your DialogFlow account
        msg_neural_gen(input_text, dialog_flow=True)  # works only if is True

    '''

class TelegramBot(threading):
    # bot's variables

    AUTHOR = ''  # author
    DESCR = ''  # description
    BOT_NAME = ''  # bot's name
    URL = ''  # the bone link for requests
    BOT_TOKEN = ''  # telegram bot token
    DF_INFO = {'session': '', 'language': '', 'id': ''}  # DialogFlow information
    processing = []  # a queue of messages to be processed

    # bot's settings, run first

    def bot_set(self,
                token,
                df_id='',
                df_session='',
                df_lang='en',
                author='',
                descr='',
                bot_name=''
                ):  # takes the information about the user's bot
        self.URL = 'https://api.telegram.org/bot' + token + '/'
        self.BOT_TOKEN = token
        self.DF_INFO['session'] = df_session
        self.DF_INFO['language'] = df_lang
        self.DF_INFO['id'] = df_id
        self.AUTHOR = author
        self.DESCR = descr
        self.BOT_NAME = bot_name
        return token, df_session, df_lang

    def msg_handler(self):  # gets the information about the
        url = self.URL + 'getupdates'  # makes a link for getting info
        get_url = requests.get(url)  # requests a link

        with open('updates.json', 'w', encoding='utf8') as file:  # encoding='utf8'
            json.dump(get_url.json(), file, indent=2, ensure_ascii=False)
        with open("updates.json", 'r', encoding='utf-8') as file_read:  # check it !!!
            data = file_read.read()
        with open("log.txt", 'w', encoding = 'utf-8') as file_log:  # creates logging file
            file_log.write(data)
        self.processing.append(get_url.json())  # adds to queue a dict with all the info about the message

