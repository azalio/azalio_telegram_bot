#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import telegramm_bot
from fake_useragent import UserAgent
import mongo
import config


def get_urls(account):
    data = {}
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    url = 'http://instagram.com/{0}/media'.format(account)
    media = requests.get(url, headers=headers).json()
    for item in media["items"]:
        data[item['created_time']] = [item['images']['standard_resolution']['url'], item['link']]
    return data


def main():
    accounts = config.conf['instagram']['accounts']

    client, db, collection = mongo.mongo_connect('instagramm', 'media')

    for account in accounts:
        data = get_urls(account)
        for date in data:
            insta_url = data[date].pop()
            img_url = data[date].pop()
            id = mongo.ObjectId(str(insta_url[-1:-13:-1]))

            if mongo.check_id(id, collection):
                post = {"_id": id,
                        "author": account,
                        "date": date,
                        "img_url": img_url,
                        "insta_url": insta_url}

                collection.insert_one(post)
                media = requests.get(img_url, stream=True)
                if media.status_code == 200:
                    path = '/tmp/' + date + '.jpeg'
                    with open(path, 'wb') as f:
                        for chunk in media.iter_content(1024):
                            f.write(chunk)
                        telegramm_bot.send_message(path, type='photo')


if __name__ == '__main__':
    main()
