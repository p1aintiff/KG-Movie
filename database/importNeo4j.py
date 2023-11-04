import json
import time

from neo4j import GraphDatabase


class JSONToNeo4jImporter:

    def __init__(self, uri, user, password, path):
        """
        初始化
        :param uri:
        :param user:
        :param password:
        :param path: json文件路径
        """
        self.path = path
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        # 节点

        self.movieDict = {
            "name": "电影名",
            "datePublished": "发布时间",
            "description": "描述",
            "duration": "时长",
            "aggregateRating": -1.0  # 评分
        }

        self.actorDict = {
            "name": "演员名"
        }

        self.directorDict = {
            "name": "导演名"
        }

        self.typeDict = {
            "genre": "类型名"
        }

    def close(self):
        self.driver.close()

    def createOneMovie(self, session, movieDict):
        """
        添加一个电影节点
        :param session: 会话
        :param movieDict: 节点属性的字典
        :return: None
        """
        movie_name = movieDict['name']
        date_published = movieDict['datePublished']
        description = movieDict['description']
        duration = movieDict['duration']
        rating = movieDict['aggregateRating']

        query = """
        MERGE (m:Movie {
            name: $name,
            datePublished: $datePublished,
            description: $description,
            duration: $duration,
            rating: $rating
        })
        """
        session.run(query, name=movie_name, datePublished=date_published, description=description,
                    duration=duration, rating=rating)

    def createOneActor(self, session, actorDict):
        """
        添加一个演员节点
        :param session: 会话
        :param actorDict: 节点属性的字典
        :return: None
        """

        # 创建演员节点
        query = "MERGE (a:Actor {name: $name})"
        session.run(query, name=actorDict['name'])

    def createOneDirector(self, session, directorDict):
        """
        添加一个导演节点
        :param session: 会话
        :param directorDict:  节点属性的字典
        :return: None
        """
        # 创建导演节点
        query = "MERGE (d:Director {name: $name})"
        session.run(query, name=directorDict['name'])

    def createOneWriter(self, session, writerDict):
        """
        添加一个编剧节点
        :param session: 会话
        :param writerDict:  节点属性的字典
        :return: None
        """
        # 创建导演节点
        query = "MERGE (w:Writer {name: $name})"
        session.run(query, name=writerDict['name'])

    def createOneType(self, session, typeDict):
        """
        添加一个类型节点
        :param session: 会话
        :param typeDict:  节点属性的字典
        :return: None
        """
        # 创建导演节点
        query = "MERGE (t:Type {genre: $type})"
        session.run(query, type=typeDict['genre'])

    def relationshipActorMovie(self, session, actor_name, movie_name):
        # 创建演员和电影之间的关系（ACTED_IN）
        query = """
                    MATCH (a:Actor {name: $actor}), (m:Movie {name: $movie})
                    CREATE (a)-[:ACTED_IN]->(m)
                    """
        session.run(query, actor=actor_name, movie=movie_name)

    def relationshipDirectorMovie(self, session, director_name, movie_name):
        # 创建导演和电影之间的关系（DIRECTED）
        query = """
                   MATCH (d:Director {name: $director}), (m:Movie {name: $movie})
                   CREATE (m)-[:DIRECTED_BY]->(d)
                   """
        session.run(query, director=director_name, movie=movie_name)

    def relationshipWriterMovie(self, session, writer_name, movie_name):
        # 创建编剧和电影之间的关系（WRITTEN_BY）
        query = """
                   MATCH (w:Writer {name: $writer}), (m:Movie {name: $movie})
                   CREATE (m)-[:WRITTEN_BY]->(w)
                   """
        session.run(query, writer=writer_name, movie=movie_name)

    def relationshipTypeMovie(self, session, type_name, movie_name):
        # 创建电影和类型之间的关系（TYPE_OF）
        query = """
                   MATCH (t:Type {genre: $genre}), (m:Movie {name: $movie})
                   CREATE (m)-[:TYPE_OF]->(t)
                   """
        session.run(query, genre=type_name, movie=movie_name)

    def getJson(self, path):
        """
        读取 JSON 文件
        :param path:
        :return:
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parseJson(self, session, oneDict):

        # 深拷贝字典
        movieDict = self.movieDict.copy()
        actorDict = self.actorDict.copy()
        writerDict = self.directorDict.copy()
        directorDict = self.directorDict.copy()
        typeDict = self.typeDict.copy()

        # 提取带电影节点
        for key in movieDict:
            if key in oneDict:
                movieDict[key] = oneDict[key]
            else:
                movieDict[key] = None

        self.createOneMovie(session, movieDict)
        # 提取演员节点
        for i in range(len(oneDict['actor'])):
            for key in actorDict:
                if key in oneDict:
                    actorDict[key] = oneDict['actor'][i]
                else:
                    actorDict[key] = None
            self.createOneActor(session, actorDict)

        # 提取导演节点
        for i in range(len(oneDict['director'])):
            for key in directorDict:
                if key in oneDict:
                    directorDict[key] = oneDict['director'][i]
                else:
                    directorDict[key] = None
            self.createOneDirector(session, directorDict)

        # 编剧节点
        for i in range(len(oneDict['writer'])):
            for key in writerDict:
                if key in oneDict:
                    writerDict[key] = oneDict['writer'][i]
                else:
                    writerDict[key] = None
            self.createOneWriter(session, directorDict)

        # 类型节点
        for i in range(len(oneDict['genre'])):
            for key in typeDict:
                if key in oneDict:
                    typeDict[key] = oneDict['genre'][i]
                else:
                    typeDict[key] = None
            self.createOneType(session, typeDict)

        # 导演和电影之间的关系
        for i in range(len(oneDict['director'])):
            self.relationshipDirectorMovie(session, oneDict['director'][i], oneDict['name'])

        # 编剧和电影之间的关系
        for i in range(len(oneDict['writer'])):
            self.relationshipWriterMovie(session, oneDict['writer'][i], oneDict['name'])

        # 演员和电影之间的关系
        for i in range(len(oneDict['actor'])):
            self.relationshipActorMovie(session, oneDict['actor'][i], oneDict['name'])

        # 类型和电影之间的关系
        for i in range(len(oneDict['genre'])):
            genre = oneDict['genre'][i]
            self.relationshipTypeMovie(session, genre, oneDict['name'])

    def run(self):
        """
        运行
        :return:
        """
        start_time = time.time()
        session = self.driver.session()
        for oneMovie in self.getJson(self.path):
            self.parseJson(session, oneMovie)
        importer.close()
        end_time = time.time()
        print("运行时间：", end_time - start_time)


if __name__ == "__main__":
    path = "/home/edmond/pythonProject/Knowledge-Graph/InfoJson/parse_unique_time.json"
    importer = JSONToNeo4jImporter("bolt://localhost:7687", "neo4j", "password", path)
    importer.run()
