# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # director = scrapy.Field()  # 导演
    # writer = scrapy.Field()  # 编剧
    # actors = scrapy.Field()  # 主演
    # genre = scrapy.Field()  # 类型
    # regions = scrapy.Field()  # 国家
    # language = scrapy.Field()  # 语言
    # releaseDate = scrapy.Field()  # 上映日期
    # duration = scrapy.Field()  # 片长（国内）
    # alternative_titles = scrapy.Field()  # 又名
    # imdb_id = scrapy.Field()  # IMDb编号
    # score = scrapy.Field()  # 评分
    raw = scrapy.Field()  # json 数据
    parse = scrapy.Field()  # json+ld 数据
    html = scrapy.Field()  # html 数据
    # id = scrapy.Field()  # id
    url = scrapy.Field()  # url