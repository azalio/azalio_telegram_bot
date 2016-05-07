#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import config

KEY = config.conf['telegram']['key']
USER_ID = config.conf['telegram']['user_id']
bot = telepot.Bot(KEY)


def send_message(data, type):
    if type == 'text':
        bot.sendMessage(USER_ID, data)
    if type == 'photo':
        data = open(data, 'r')
        bot.sendPhoto(USER_ID, data)


def main():
    pass


if __name__ == '__main__':
    main()
