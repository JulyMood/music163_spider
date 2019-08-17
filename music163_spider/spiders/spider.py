from __future__ import absolute_import
import scrapy, re
from items import Music163SpiderItem


class Spider(scrapy.Spider):
    name = 'music163_spider'
    root = 'https://music.163.com'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover/playlist']
    limit = 35
    max_page = 38

    def parse(self, response):
        tags = response.selector.xpath('//div[@class="bd"]/dl/dd/a/@href').extract()
        for tag in tags:
            for i in range(0, self.max_page):
                offset = i * self.limit
                pages_url = self.root + tag + '&limit={0}&offset={1}'.format(self.limit, offset)
                yield scrapy.Request(pages_url, method='GET', callback=self.parse_playlist)

    def parse_playlist(self, response):
        songs_list = response.selector.xpath('//div[@class="u-cover u-cover-1"]/a/@href').extract()
        for songs in songs_list:
            yield scrapy.Request(self.root + songs, method='GET', callback=self.parse_songs)

    def parse_songs(self, response):
        songs = re.findall('(?<=\<span class="txt"><a href=").*?(?=\"><b title=)', response.text)
        tags = response.selector.xpath('//div[@class="tags f-cb"]/a[@class="u-tag"]/i/text()').extract()
        for song in songs:
            yield scrapy.Request(self.root + song, method='GET',
                                 callback=lambda response, tags=tags: self.parse_song(response, tags))

    def parse_song(self, response, tags):
        item = Music163SpiderItem()
        lyrics_1 = response.selector.xpath('//div[@id="lyric-content"]/text()').extract()
        lyrics_2 = response.selector.xpath('//div[@id="flag_more"]/text()').extract()
        item['b_singer'] = response.selector.xpath('//div[@class="cnt"]/p/span/a/text()').extract_first()
        item['a_song_name'] = response.selector.xpath('//em[@class="f-ff2"]/text()').extract_first()
        item['f_lyrics'] = lyrics_1 + lyrics_2
        item['e_tags'] = ','.join(tags)
        if item['f_lyrics'] is None or item['b_singer'] is None \
                or item['a_song_name'] is None or item['e_tags'] is None:
            return None
        item['c_composer'] = process_lyrics(item['f_lyrics'], '作曲')
        item['d_lyricist'] = process_lyrics(item['f_lyrics'], '作词')
        item['f_lyrics'] = list(filter(lambda x: x.find(':') == -1 and x.find('：') == -1, item['f_lyrics']))
        if item['f_lyrics'] is None or len(item['f_lyrics']) < 10:
            return None
        item['f_lyrics'] = ','.join(item['f_lyrics'])
        yield item


def process_lyrics(lyrics, key):
    temp = list(filter(lambda x: x.find(key) != -1 and (x.find(':') != -1 or x.find('：') != -1), lyrics))
    if temp is not None and len(temp) > 0:
        if temp[0].find(':') != -1:
            return temp[0].split(':')[-1].strip()
        elif temp[0].find('：') != -1:
            return temp[0].split('：')[-1].strip()
    return '-'
