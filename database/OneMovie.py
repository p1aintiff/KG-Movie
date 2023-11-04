import json
from database.DBneo4j import Neo4j


class Movies:
    def __init__(self):

        self.db = Neo4j("../database/DB.json")
        self.tem = {
            "name": "",
            "director": [None],
            "writer": [None],
            "actor": [None],
            "datePublished": "",
            "genre": [None],
            "duration": 0,
            "description": "",
            "rating": ""
        }

        self.movieInfos = []

    #
    # def parseResult(self, result, infoDict=None):
    #     """
    #     把查询结果转换成self.tem的格式
    #     :param result:
    #     :param infoDict:
    #     :return:
    #     """
    #     if infoDict is None:
    #         infoDict = self.tem.copy()
    #     # todo 模板文件不适合演员解析
    #     for key in self.tem.keys():
    #
    #         infoDict['actor'].append(result.get("name"))
    #
    #     return infoDict

    def getMovieNodes(self, name):
        """
        根据电影名称查询电影节点
        :param name:
        :return:
        """
        results = self.db.queryMovieByName(name)
        for result in results:
            infoDict = self.tem.copy()
            for key in self.tem.keys():
                if result.get(key) is not None:
                    infoDict[key] = result.get(key)
            self.movieInfos.append(infoDict)

    def getActorNodes(self, movieInfo):
        """
        根据电影节点查询演员节点
        :param movieInfo:
        :return:
        """
        results = self.db.nodeToNode(movieName=movieInfo.get("name"), genre="ACTED_IN")
        for result in results:
            movieInfo['actor'].append(result.get("name"))

    def getInfoJson(self):
        """
        返回电影信息的json
        :return:
        """
        js = json.dumps(self.movieInfos, ensure_ascii=False, indent=4)
        self.movieInfos = None
        return js

    def getMovieInfos(self):

        infos = self.movieInfos
        self.movieInfos = []
        return infos

    def run(self, name):
        self.getMovieNodes(name)
        for movieInfo in self.movieInfos:
            self.getActorNodes(movieInfo)


movies = Movies()

if __name__ == '__main__':
    movies = Movies()
    movies.run("同级生")
    print("结果", movies.getInfoJson())
