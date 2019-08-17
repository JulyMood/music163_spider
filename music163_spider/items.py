# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    b_singer = scrapy.Field()
    a_song_name = scrapy.Field()
    e_tags = scrapy.Field()
    f_lyrics = scrapy.Field()
    c_composer = scrapy.Field()
    d_lyricist = scrapy.Field()
