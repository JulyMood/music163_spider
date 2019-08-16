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
        item['singer'] = response.selector.xpath('//div[@class="cnt"]/p/span/a/text()').extract_first()
        item['song_name'] = response.selector.xpath('//em[@class="f-ff2"]/text()').extract_first()
        item['lyrics'] = lyrics_1 + lyrics_2
        item['tags'] = ','.join(tags)
        yield item
