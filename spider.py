# -*- coding: utf-8 -*-
import json
from multiprocessing import Pool

import settings
from utils import get_page
from utils import soup_movie_page
from DB import monve_db


class Douban_movic(object):


    def __init__(self):
        self.first_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={page}'
        self.contrnue_run = True


    def parse_index(self,datas):
        datas_num = len(datas.get('data'))
        if datas_num > 0 :
            # for data in datas.get('data'):
            #     page_url = data['url']
            #     self.parse_page(page_url)
        #多进程
            pool = Pool(4)
            for data in datas.get('data'):
                pages_url = data['url']
                pool.apply_async(self.parse_page, args=(pages_url,))
            pool.close()
            pool.join()
        else:
            self.contrnue_run = False


    def parse_page(self,url):
        context = get_page(url = url)
        item = soup_movie_page(context)
        db =monve_db()
        db.DB_open()
        db.update_item(item)
        print(item)

    def run(self):
        page = get_index()
        while self.contrnue_run:

            url = self.first_url.format(page = page)
            context = get_page(url = url)
            try:
                datas = json.loads(context)
            except TypeError:
                print('TypeError')
            if len(datas.get('data')) > 0:
                self.parse_index(datas)
                page = page + 20
                set_index(page = page)


def get_index(path = './page.ini'):
    with open(path,'r+') as f:
        page = f.read()
        print('get page :',page)
        return int(page)

def set_index(path = './page.ini',page = 0):
    with open(path,'w+') as f:
        print('set page :',page)
        f.write(str(page))