import copy
import json
import os
import pandas
import re

"""
输入文件路径，将json先set去重，再转换为list原地储存
"""


def uniqueJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        original_list = json.load(f)

    # 将字典列表转换为 JSON 字符串并去重
    unique_set = set(json.dumps(d, sort_keys=True) for d in original_list)

    # 将 JSON 字符串转回为字典，得到去重的字典列表
    unique_list = [json.loads(s) for s in unique_set]

    savePath = path.replace('.json', '_unnique.json')
    with open(savePath, 'w', encoding='utf-8') as f:
        json.dump(unique_list, f, ensure_ascii=False, indent=4)

    print('origin: ' + str(len(original_list)))
    print('unique: ' + str(len(unique_list)))


def allToCsv(rawPath):
    # 打开目录下所有json文件
    # 每一个字典是一行记录，每一个键值对是一列属性
    # 如果字典的值是列表，使用%%连接，将列表转换为字符串

    for root, dirs, files in os.walk(rawPath):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for i in range(len(data)):
                        for key in data[i]:
                            if type(data[i][key]) is str:
                                data[i][key] = data[i][key].replace("['", '').replace("']", '').replace("', '", '%%')
                    data = pandas.DataFrame(data)
                    data.to_csv('./washedCsv/' + file[:-5] + '.csv', index=False, encoding='utf-8')
                    print(file[:-5] + '.csv' + '已生成')


def allToJson(rawPath):
    # 将csv文件转换为json文件
    # 读取csv文件
    # 将每一行转换为字典
    # 将字典写入json文件
    # 保存json文件
    for root, dirs, files in os.walk(rawPath):
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f1:
                    data = pandas.read_csv(f1, encoding='utf-8')
                    data = data.to_dict(orient='records')
                    with open('./washedJson/' + file[:-4] + '.json', 'w', encoding='utf-8') as f2:
                        json.dump(data, f2, ensure_ascii=False, indent=1)
                        print(file[:-4] + '.json' + '已生成')


class Wash:
    def __init__(self) -> None:
        self.rawDir = '/home/edmond/douban/json/'
        self.outDir = '/home/edmond/douban/washDate/'

    # 获取rawDir下的所有文件名
    def everyFile(self):
        fileNames = os.listdir(self.rawDir)
        for file in fileNames:
            yield file

    # 读取json文件
    def getJson(self, onePath):
        with open(onePath, 'r') as f:
            data = json.load(f)
        return data

    # 将数据保存为json文件
    def saveJson(self, data, onePath):
        outPath = self.outDir + onePath
        with open(outPath, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # 读取说有id，并保存为json文件
    def outId(self):
        for onePath in self.everyFile():
            data = self.getJson(self.rawDir + onePath)
            oneJson = OneJson(data)
            idList = oneJson.getIds()
            self.saveJson(idList, 'id/' + onePath)

    # 输出简化后的数据
    def outBrief(self):
        for onePath in self.everyFile():
            data = self.getJson(self.rawDir + onePath)
            oneJson = OneJson(data)

            newData = oneJson.wash()
            self.saveJson(newData, 'json/' + onePath)


class OneJson:
    def __init__(self, rawData) -> None:
        # 原始数据
        self.rawData = rawData

        # 储存数据
        self.data = []
        self.oneMovie = {
            'title': None,  # 片名
            'types': None,  # 类别
            'release_date': None,  # 上映时间
            'regions': None,  # 拍摄国家
            'score': None,  # 评分
            # 'director': None,   # 导演
            'actors': None,  # 演员
        }

    def getInfo(self):
        length = len(self.rawData)
        print('共有{}条数据'.format(length))

    def wash(self):
        # 根据onemovie的key，获取数据
        for i in range(len(self.rawData)):
            oneMovie = copy.deepcopy(self.oneMovie)
            for key in oneMovie:
                oneMovie[key] = self.rawData[i][key]
            self.data.append(oneMovie)
        print(len(self.data))
        return self.data

    # 提取出所有id，放在一个列表中，最后储存在json文件中
    def getIds(self):
        ids = []
        for i in range(len(self.rawData)):
            ids.append(self.rawData[i]['id'])
        return ids


# 打开rawjson文件中的所有json文件
def get_json():
    json_path = os.path.join(os.getcwd(), 'rawJson')
    json_list = os.listdir(json_path)
    return json_list


# 获取json文件中的url
def get_url(json_list):
    url_list = []
    for json_file in json_list:
        json_path = os.path.join(os.getcwd(), 'rawJson', json_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            json_dict = json.load(f)
            for i in json_dict:
                url_list.append(i['url'])
    return url_list


# 将url列表写入json，放在scrapy项目的根目录下
def write_url(url_list):
    with open('scrapyInfo/url.json', 'w', encoding='utf-8') as f:
        json.dump(url_list, f, ensure_ascii=False, indent=1)




def parse_duration(duration):
    hours = 0
    minutes = 0

    # 使用正则表达式从字符串中提取小时和分钟
    hours_match = re.search(r'(\d+)H', duration)
    minutes_match = re.search(r'(\d+)M', duration)

    # 如果匹配成功，提取小时和分钟的值
    if hours_match:
        hours = int(hours_match.group(1))
    if minutes_match:
        minutes = int(minutes_match.group(1))

    # 将小时转换为分钟并加上分钟数
    total_minutes = hours * 60 + minutes
    return total_minutes


def transTime(path):
    with open(path, 'r', encoding='utf-8') as f:
        js = json.load(f)
        for movie in js:
            duration = movie.get('duration')
            print(duration)
            movie['duration'] = parse_duration(duration)
            print(movie['duration'])

    

    newPath = path.replace('.json', '_time.json')
    with open('./parse_unique_time.json', 'w', encoding='utf-8') as f:
        json.dump(js, f, ensure_ascii=False, indent=1)
    print('over')
    





if __name__ == '__main__':
    rawPath = 'InfoJson/parse_new.json'
    transTime(rawPath)