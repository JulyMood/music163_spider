# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import hashlib


class Music163SpiderPipeline(object):
    def __init__(self):
        self.song_set = set()

    def process_item(self, item, spider):
        if item['lyrics'] is None or item['singer'] is None or item['song_name'] is None or item['tags']:
            return None
        item['lyrics'] = list(filter(lambda x: x.find(':') == -1 and x.find('：') == -1, item['lyrics']))
        if item['lyrics'] is None or len(item['lyrics']) < 10:
            return None
        first_lyrics = item['lyrics'][0]
        song_key = hashlib.md5((item['song_name'] + first_lyrics).encode(encoding='UTF-8')).hexdigest()
        if song_key in self.song_set:
            return None
        item['lyrics'] = ','.join(item['lyrics'])
        self.song_set.add(song_key)
        data = pd.DataFrame([item])
        data.to_csv('/tmp/data.csv', encoding='gbk', mode='a', index=False, header=False)
        return item
