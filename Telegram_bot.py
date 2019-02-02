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


class TelegramBot:

    DF_INFO = {'session': '', 'language': '', 'id': ''}  # DialogFlow information

    def __init__(self,
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
        self.processing = []  # a queue of messages to be processed
        return token, df_session, df_lang

    def __json_collect(self, to_conv):  # turns a json dict into the file
        with open('updates.json', 'w', encoding='utf8') as file:  # encoding='utf8'
            json.dump(to_conv, file, indent=2, ensure_ascii=False)

    def logging(self):
        if not path.isfile("updates.json"):
            with open('log.txt', 'r', encoding='utf-8') as log:
                data = log.read()
            with open('updates.json', 'w', encoding='utf-8') as file:
                file.write(data)

    def get_info(self):  # gets the information about the
        url = self.URL + 'getupdates'  # makes a link for getting info
        get_url = requests.get(url)  # requests a link

        self.__json_collect(get_url.json())  # creates a json file on the computer
        with open("updates.json", 'r', encoding='utf-8') as file_read:
            data = file_read.read()
        with open("log.txt", 'w', encoding = 'utf-8') as file_log:
            file_log.write(data)
        self.processing.append(get_url.json())  # adds to queue a dict with all the info about the message

        return get_url.json()

    def msg_send(self, chat_id, text, error_response='<Error>: response text is missing'):  # sends the message
        if str(text) != '':
            response = str(text)
        else:
            response = error_response
        send_msg_url = self.URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, response)
        requests.get(send_msg_url)  # makes a request for sending the message

    def msg_neural_gen(self,input_text, dialog_flow=True):  # generates the message using NeuralNetwork
        if dialog_flow:
            df = apiai.ApiAI(self.DF_INFO['id']).text_request()
            df.lang = self.DF_INFO['language']
            df.session_id = self.DF_INFO['session']  # session id
            df.query = input_text
            response_json = json.loads(df.getresponse().read().decode('utf-8'))  # cover out the json file
            response = response_json['result']['fulfillment']['speech']  # response = the text of response message
            return response

    def info(self, search):  # returns the information about the bot
        information = {'token_info': self.BOT_TOKEN,  # bot's token
                'last_msg_info': self.get_info()['result'][-1],  # a full info about the last message
                'last_msg_info_short': {  # a list with last_msg chat ID and text
                    'chat_id_info': self.get_info()['result'][-1]['message']['chat']['id'],
                    'text_info': self.get_info()['result'][-1]['message']['text']
                },
                'bot_info': {
                    'description': str(self.DESCR),
                    'author' : str(self.AUTHOR),
                    'name': str(self.BOT_NAME)
                },  # a full information about the bot
                }  # returns your bot token
        return information[search]
