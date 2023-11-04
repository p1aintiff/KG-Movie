import random
import re
import time

import requests
import json
from lxml import etree


class GetSexy:
    def __init__(self):
        self.urlPath = 'url.json'
        self.parsePath = 'parse.json'
        self.rawPath = 'raw.json'
        self.urls = []
        self.parseData = []
        self.rawData = []
        self.oneData = {
            'name': '',
            'director': [],
            'writer': [],
            'actor': [],
            'datePublished': '',
            'genre': [],
            'duration': '',
            'description': '',
            'aggregateRating': ''

        }

    def start_requests(self):

        print('urls' + str(len(self.urls)))

        for url in self.urls:
            yield url

    def sendRequest(self, url):
        """"""
        hearders = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'll="108288"; bid=h5IWoHLGzNo; _pk_id.100001.4cf6=0e6bdd5434ea5c47.1697878758.; __utmz=30149280.1697878761.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmz=223695111.1697878761.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=DE7C12C74CB629B81C62044217F56FE90|07e2c2c285ac1cf4ed21d19574ee60e9; dbcl2="275307411:TS85krFajRc"; push_noty_num=0; push_doumail_num=0; __yadk_uid=trrDIBHFKq3QhxdxMCgY1jOsIKT3oziY; __utmv=30149280.27530; ck=HokW; frodotk_db="e6cb5504e10028a1b461ff0ea30079e3"; ap_v=0,6.0; __utma=30149280.1202521683.1697878761.1697894618.1697947273.5; __utmc=30149280; __utma=223695111.1686675.1697878761.1697894618.1697947273.5; __utmc=223695111',
            'Host': 'movie.douban.com', 'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'}

        # proxy = {
        #     "http": "http://127.0.0.1:7890",
        #     "https": "http://127.0.0.1:7890"
        # }
        # verify_ssl = True

        # todo 使用你自己的代理
        proxy = {}
        verify_ssl = False

        response = requests.get(url, headers=hearders, proxies=proxy, verify=verify_ssl)
        return response

    def parse(self, response):
        html = response.text

        root = etree.HTML(html)

        # 提取包含 JSON-LD 数据的脚本标签
        jsonLd = ''
        try:
            jsonLd = root.xpath('/html/head/script[@type="application/ld+json"]/text()')[0].replace('\n', '')
        except IndexError as e:
            print(e)

        # 解析 JSON-LD 数据
        if jsonLd:
            try:
                jsonDict = json.loads(jsonLd)
            except json.decoder.JSONDecodeError as e:
                print(e)
                jsonLd = jsonLd.replace('\r', '').replace('\n', '').replace('\t', '')
                jsonDict = json.loads(jsonLd)

            url = jsonDict.get('url', '')
            if 'https://movie.douban.com' not in url:
                url = 'https://movie.douban.com' + url
            self.unique(url)
            # 提取电影名称、导演、编剧等信息
            name = jsonDict.get('name', '')
            director = [item.get('name', '') for item in jsonDict.get('director', [])]
            writer = [item.get('name', '') for item in jsonDict.get('author', [])]
            actor = [item.get('name', '') for item in jsonDict.get('actor', [])]
            datePublished = jsonDict.get('datePublished', '')
            genre = jsonDict.get('genre', [])
            duration = jsonDict.get('duration', '')
            description = jsonDict.get('description', '')
            aggregateRating = jsonDict.get('aggregateRating', {}).get('ratingValue', '')

            # 创建一个包含提取信息的数据项（item）
            self.oneData = {
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

            self.parseData.append(self.oneData)
            self.rawData.append(jsonLd)

    def getLocalData(self):
        with open(self.parsePath, 'r', encoding='utf-8') as f:
            self.parseData = json.load(f)
        with open(self.rawPath, 'r', encoding='utf-8') as f:
            self.rawData = json.load(f)

        with open('url.json', 'r', encoding='utf-8') as f:
            self.urls = json.load(f)

    def save(self):
        # 写入 JSON 文件
        with open(self.parsePath, 'w', encoding='utf-8') as f:
            json.dump(self.parseData, f, ensure_ascii=False, indent=4)

        # 写入 JSON-LD 文件
        with open(self.rawPath, 'w', encoding='utf-8') as f:
            json.dump(self.rawData, f, ensure_ascii=False, indent=4)

        with open(self.urlPath, 'w', encoding='utf-8') as f:
            json.dump(self.urls, f, ensure_ascii=False, indent=4)

    def unique(self, url):
        if url in self.urls:
            self.urls.remove(url)
            print('remove:  ' + url)

    def run(self):
        self.getLocalData()
        for url in self.start_requests():
            # 停顿随即0-1秒
            time.sleep(random.random())
            response = self.sendRequest(url)
            self.parse(response)
            self.save()


if __name__ == '__main__':
    getSexy = GetSexy()
    getSexy.run()
