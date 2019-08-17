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
        first_lyrics = item['f_lyrics'][0]
        song_key = hashlib.md5((item['a_song_name'] + first_lyrics).encode(encoding='UTF-8')).hexdigest()
        if song_key in self.song_set:
            return None
        self.song_set.add(song_key)
        data = pd.DataFrame([item])
        data.to_csv('/tmp/song.csv', encoding='gbk', mode='a', index=False, header=False)
        return item
