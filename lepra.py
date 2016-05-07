#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
from BeautifulSoup import BeautifulSoup
import re
import mongo
import telegramm_bot
import config


def get_posts(site):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    uid = config.conf['lepra']['uid']
    sid = config.conf['lepra']['sid']
    cookies = {'uid': uid, 'sid': sid}
    url = 'https://{0}.leprosorium.ru/'.format(site)
    r = requests.get(url, headers=headers, cookies=cookies)
    if r.status_code == 200:
        return r.text


def clear_post(post):
    post = post.replace('<br />', '\n')
    post = post.replace('<div class="dti p_body">', '')
    post = post.replace('/div', ' ')
    post = post.replace('<b>', ' ')
    post = post.replace('</b>', ' ')
    post = post.replace('<sub>', ' ')
    post = post.replace('</sub>', ' ')
    post = post.replace('">', ' ')
    post = post.replace('</a>', ' ')
    post = post.replace('" height=.*/>', ' ')
    post = post.replace('" width=.*/>', ' ')
    post = post.replace('<span class="', ' ')
    post = post.replace('</span>', ' ')
    post = post.replace('< >', '\n')
    post = post.replace('<i>', ' ')
    post = post.replace('</i>', ' ')
    post = post.replace('" alt="image', ' ')
    post = re.sub(r'<a target="_blank" href="', ' ', post)
    post = re.sub(r'<img src="', ' ', post)
    post = re.sub(r'" width="[0-9]+" height="[0-9]+" />', ' ', post)
    post = re.sub(r'<img .*src="', ' ', post)
    post = re.sub(r'" title=.*KB', ' ', post)
    post = re.sub(r'" rel="youtube".*data-start_time="0', ' ', post)
    post = re.sub(r'" alt=".*kb', ' ', post)

    return post


# sites = ['baraholka', 'idiod']
sites = config.conf['lepra']['sites']
db_name = config.conf['lepra']['db_name']

for site in sites:
    client, db, collection = mongo.mongo_connect(db_name, site)

    html = get_posts(site)
    soup = BeautifulSoup(html)
    results = soup.findAll("div", {"class": re.compile("^(post.*)$")})
    for post_html in results:
        post = post_html.find('div', {'class': 'dti p_body'})
        url = post_html.find('span', {'class': 'b-post_comments_links'}).a.get('href')

        post = str(post)
        post = clear_post(post)
        url = 'https:' + url
        id = mongo.ObjectId(str(url[-1:-13:-1]))
        if mongo.check_id(id, collection):
            post_json = {"_id": id,
                         "url": url,
                         "post": post}
            collection.insert_one(post_json)
            post = str(post) + '\n' + str(url)
            telegramm_bot.send_message(post, type='text')
