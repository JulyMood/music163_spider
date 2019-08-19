# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import hashlib
import redis


class Music163SpiderPipeline(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='*', password='*',
                                    port=6379, db=0)
        self.r = redis.Redis(connection_pool=pool)

    def process_item(self, item, spider):
        first_lyrics = item['f_lyrics'][0]
        song_key = str(hashlib.md5((item['a_song_name'] + first_lyrics).encode(encoding='UTF-8')).hexdigest())
        distinct = self.r.setnx(song_key, 1)
        if distinct:
            self.r.expire(song_key, 60 * 60 * 60 * 23 * 3)
        else:
            print('distinct : ' + item['a_song_name'])
            return None
        data = pd.DataFrame([item])
        data.to_csv('/Users/zhangkai/Documents/lyrics.csv', encoding='gbk', mode='a', index=False, header=False)
        return item
