import random

import re
import requests
import time

from bs4 import BeautifulSoup

import settings

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


proxies = {'http':'http://111.155.116.239:8123'}



def get_page(url):
    headers['User-Agent'] = random_user_agent()
    print(headers)
    print('Getting', url)
    try:
        r = requests.get(url, headers = headers, proxies=proxies)
        time.sleep(settings.REQUEST_SLEEP_TIME)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


def random_user_agent():
    userAgent = random.choice(settings.USER_AGENTS)
    return userAgent

def get_text(context):
    lis = []
    for item in context:
        lis.append(item.text)
    return lis

def soup_movie_page(context):
    soup = BeautifulSoup(context,'lxml')

    title = soup.select('#content > h1 > span')[0].text#电影名字

    year = soup.select('#content > h1 > span')[1].text #电影年份
    clear_year = year.strip('(').strip(')')

    directors = soup.select('a[rel="v:directedBy"]')
    director = get_text(directors)#电影导演

    starring = soup.select('a[rel="v:starring"]')
    starrings = get_text(starring)#演员

    movie_type = soup.select('span[property="v:genre"]')#类型
    movie_types = get_text(movie_type)

    releaseDate = soup.select('span[property="v:initialReleaseDate"]')#上映日期
    releaseDates = get_text(releaseDate)

    source = soup.select('strong[property="v:average"]')[0].text#评分

    star = soup.select('div[class="ratings-on-weight"] > .item > span.rating_per')
    stars = get_text(star)

    start_dic = {}#1--5分评分率
    for i in range(0,5):
        start_dic['{}start'.format(5-i)] = float(stars[i].strip('%'))

    description = soup.select('span[property="v:summary"]')[0].text

    return {
        'title':title,
        'year':int(clear_year),
        'director':director,
        'starrings':starrings,
        'movie_types':movie_types,
        'releaseDates':releaseDates,
        'source':float(source),
        'start_dic':start_dic,
        'description':description
    }
