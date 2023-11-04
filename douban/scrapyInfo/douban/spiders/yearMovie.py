import re
import scrapy
from ..items import DoubanItem
import json


class yearMovie(scrapy.Spider):
    name = "yearMovie"
    allowed_domains = ["movie.douban.com"]

    # 设置下载超时时间为30秒
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 15  # 单位为秒
    }

    def start_requests(self):
        urls = []
        with open('url.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
        print('urls' + str(len(urls)))

        for url in urls[:111]:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        ###########

        item = DoubanItem()
        item['html'] = response.text
        item['name'] = response.xpath('//title/text()').get()

        # 提取包含 JSON-LD 数据的脚本标签

        scriptTag = response.xpath('/html/head/script[@type="application/ld+json"]').get()
        json_match = ''
        if scriptTag:
            json_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', scriptTag, re.DOTALL)
        else:
            print('*' * 20)
        # 解析 JSON-LD 数据
        if json_match:
            json_str = json_match.group(1).replace('\n', '')
            item['raw'] = json.loads(json_str)
            json_data = json.loads(json_str)
            item['url'] = item['raw'].get('url', '')

            # if (script_data):
            #     item['raw'] = json.loads(script_data)
            #     json_data = json.loads(script_data)

            # 提取电影名称、导演、编剧等信息
            name = json_data.get('name', '')  # 电影名称
            director = [item.get('name', '') for item in json_data.get('director', [])]  # 导演
            writer = [item.get('name', '') for item in json_data.get('author', [])]  # 编剧
            actor = [item.get('name', '') for item in json_data.get('actor', [])]  # 演员
            datePublished = json_data.get('datePublished', '')  # 上映日期
            genre = json_data.get('genre', [])  # 电影类型
            duration = json_data.get('duration', '')  # 电影时长
            description = json_data.get('description', '')  # 电影简介
            aggregateRating = json_data.get('aggregateRating', {}).get('ratingValue', '')  # 电影评分

            # 创建一个包含提取信息的数据项（item）
            item['parse'] = {
                'name': name,
                'director': director,
                'writer': writer,
                'actor': actor,
                'datePublished': datePublished,
                'genre': genre,
                'duration': duration,
                'description': description,
                'aggregateRating': aggregateRating
            }

            # 可以将 movie_item 保存到数据库或进行其他处理
            yield item
