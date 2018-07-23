#  -*- coding: utf-8 -*-
from Telegram_bot import TelegramBot  # telegram bot module
from config import telegram_token, dialog_flow_token  # telegram bot and DialogFlow tokens


def main():

    def dialog_flow_response():
        my_bot.msg_send(my_bot.info('last_msg_info_short')['chat_id_info'],
                        my_bot.msg_neural_gen(my_bot.info('last_msg_info_short')['text_info']))

    my_bot = TelegramBot()  # creates a bot-object
    my_bot.bot_set(  # sets the information
        telegram_token,
        dialog_flow_token,
        'OsamaBinLadenBot',
        'ru'
    )
    my_bot.logging()  # logs, if the programme has stopped
    last_msg_update = my_bot.info('last_msg_info')['update_id']  # writes update id
    while True:
        while last_msg_update != my_bot.info('last_msg_info')['update_id']:  # if update id has changed
            my_bot.get_info()  # updates the information about the last message
            dialog_flow_response()  # msg send
            last_msg_update = my_bot.info('last_msg_info')['update_id']


if __name__ == '__main__':
    main()
