# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface

import json
import os


class DoubanPipeline:
    def open_spider(self, spider):

        # 解码后的 JSON 数据
        self.parsePath = 'parse.json'
        self.parseData = []

        # 如果文件不存在，创建一个空的 JSON 文件
        if not os.path.isfile(self.parsePath):
            with open(self.parsePath, 'w', encoding='utf-8') as f1:
                f1.write('[]')
        # 打开 JSON 文件并加载数据
        with open(self.parsePath, 'r', encoding='utf-8') as f1:
            self.parseData = json.load(f1)

        # 未解码的 JSON-LD 数据
        self.rawPath = 'raw.json'
        self.rawData = []

        # 打开 JSON-LD 文件并加载数据
        if not os.path.isfile(self.rawPath):
            with open(self.rawPath, 'w', encoding='utf-8') as f2:
                f2.write('[]')
        with open(self.rawPath, 'r', encoding='utf-8') as f2:
            self.rawData = json.load(f2)

        # 删除url列表中已经爬取的url
        with open('url.json', 'r', encoding='utf-8') as f:
            self.uncatched = json.load(f)

    def process_item(self, item, spider):
        # 储存json数据
        self.rawData.append(item['raw'])
        self.parseData.append(item['parse'])


        # 储存原始html
        name = item['parse'].get('name', '')
        with open('./htmls/' + name + '.html', 'w', encoding='utf-8') as f:
            f.write(item['html'])

        if 'https://movie.douban.com' not in item['url']:
            item['url'] = 'https://movie.douban.com' + item['url']

        # 删除url列表中已经爬取的url
        if item['url'] in self.uncatched:
            self.uncatched.remove(item['url'])

        return item

    def close_spider(self, spider):
        # 写入 JSON 文件
        with open(self.parsePath, 'w', encoding='utf-8') as f:
            json.dump(self.parseData, f, ensure_ascii=False, indent=4)

        # 写入 JSON-LD 文件
        with open(self.rawPath, 'w', encoding='utf-8') as f:
            json.dump(self.rawData, f, ensure_ascii=False, indent=4)

        print('---'*100)

        self.uncatched = list(set(self.uncatched))
        print(len(self.uncatched))
        with open('url.json', 'w', encoding='utf-8') as f:
            json.dump(self.uncatched, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pip = DoubanPipeline()
    items = {
        'raw': {
            'name': 'raw'
        },
        'parse': {
            'name': 'parse'
        }
    }
    pip.open_spider('spider')
    pip.process_item(items, 'spider')
    pip.close_spider('spider')
