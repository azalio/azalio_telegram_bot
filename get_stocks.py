import config
import telegramm_bot
import requests
from fake_useragent import UserAgent


def get_stock(name):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    url = "http://finance.yahoo.com/webservice/v1/symbols/{}/quote?format=json&view=detail".format(name)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r = r.json()
            stock_dict = {
                'issuer_name': r['list']['resources'][0]['resource']['fields']['issuer_name'],
                'price': r['list']['resources'][0]['resource']['fields']['price'],
                'chg_percent': r['list']['resources'][0]['resource']['fields']['chg_percent'],
                'change': r['list']['resources'][0]['resource']['fields']['change'],
                'utctime': r['list']['resources'][0]['resource']['fields']['utctime']
            }
        return stock_dict

    except requests.exceptions.RequestException as e:
        post = 'requests raise exception!\n' + str(url) + '\n' + str(e)
        telegramm_bot.send_message(post, type='text')
        return False
    pass


def main():
    names = config.conf['finance']['stocks']
    for name in names:
        stock_dict = get_stock(name)
        post = ''
        for key in stock_dict:
            post = post + key + ': ' + stock_dict[key] + '\n'
        telegramm_bot.send_message(post, type='text')


if __name__ == '__main__':
    main()
