from neo4j import GraphDatabase
import json


def getDBProperties(path):
    """
    从json文件中获取数据库的URL, USER, PASSWORD
    :param path: 保存数据库连接的json文件的路径
    :return: 元组(URL, USER, PASSWORD)
    """
    with open(path.replace("json", "txt"), 'w') as f:
        f.write("asd")
    with open(path, 'r') as f:
        DBProperties = json.load(f)
    return DBProperties.get("URI"), DBProperties.get("USER"), DBProperties.get("PASSWORD")


class Neo4j:
    def __init__(self, DBPropertiesPath):
        self.URI, self.USER, self.PASSWORD = getDBProperties(DBPropertiesPath)
        self._driver = GraphDatabase.driver(self.URI, auth=(self.USER, self.PASSWORD))
        self.session = self._driver.session()

    def close(self):
        self.session.close()
        self._driver.close()

    def queryNode(self, query, **kwargs):
        """
        执行查询语句
        :param query: 查询语句
        :param kwargs: 查询语句中的参数,需要输入param=value的形式
        :return: 查询结果[{"n":{}},]
        """
        if not kwargs:
            print("No parameters")
            resultsClass = self.session.run(query)
        else:
            resultsClass = self.session.run(query, **kwargs)
            # print(resultsClass.data())
        return resultsClass.data()

    def queryMovieByName(self, name, limit=10, precise=False):
        """
        根据电影名查询电影
        :param name: 电影名称
        :param limit: 结果数量
        :param precise: 是否精确查询
        :return: 电影json的列表
        """
        if precise:
            sql = "match(n:Movie{name:$name}) return n limit $limit;"
        else:
            sql = "match(n:Movie) where n.name contains $name return n limit $limit;"
        resultList = self.queryNode(sql, limit=limit, name=name)
        theList = [result.get("n") for result in resultList]
        return theList

    def queryActorByName(self, name, limit=10, precise=False):
        """
        根据演员名查询演员
        :param name: 演员名称
        :param limit: 结果数量
        :param precise: 是否精确查询
        :return: 演员json的列表
        """
        if precise:
            sql = "match(n:Actor{name:$name}) return n limit $limit;"
        else:
            sql = "match(n:Actor) where n.name contains $name return n limit $limit;"
        resultList = self.queryNode(sql, limit=limit, name=name)
        return [result.get("n") for result in resultList]

    def queryDirectorByName(self, name, limit=10, precise=False):
        """
        根据导演名查询导演
        :param name: 导演名称
        :param limit: 结果数量
        :param precise: 是否精确查询
        :return: 导演json的列表
        """
        if precise:
            sql = "match(n:Director{name:$name}) return n limit $limit;"
        else:
            sql = "match(n:Director) where n.name contains $name return n limit $limit;"
        resultList = self.queryNode(sql, limit=limit, name=name)
        return [result.get("n") for result in resultList]

    def queryMovieByType(self, movieType, limit=10):
        """
        根据电影类型查询电影
        :param movieType: 电影类型
        :param limit: 结果数量
        :return: 电影json的列表
        """
        sql = "match(n:Movie)-[r:TYPE_OF]->(t:Type{genre:$type}) return n limit $limit;"
        resultList = self.queryNode(sql, type=movieType, limit=limit)
        return [result.get("n") for result in resultList]

    def queryMovieByActor(self, actorName, limit=10):
        """
        根据演员查询电影
        :param actorName: 演员名称
        :param limit: 结果数量
        :return: 电影json的列表
        """
        sql = "match(n:Movie)-[r:ACT_IN]->(a:Actor{name:$name}) return n limit $limit;"
        resultList = self.queryNode(sql, name=actorName, limit=limit)
        return [result.get("n") for result in resultList]

    def queryMovieByDirector(self, directorName, limit=10):
        """
        根据导演查询电影
        :param directorName: 导演名称
        :param limit: 结果数量
        :return: 电影json的列表
        """
        sql = "match(n:Movie)-[r:DIRECTED_BY]->(d:Director{name:$name}) return n limit $limit;"
        resultList = self.queryNode(sql, name=directorName, limit=limit)
        return [result.get("n") for result in resultList]

    def nodeToNode(self, movieName, genre, limit=25):
        """
        查一个电影节点的关系节点
        :param movieName: 头节点名称
        :param genre: 关系类型
        :param limit: 数量限制
        :return:
        """
        if genre == "ACTED_IN":
            sql = "match(n:Actor)-[r:ACTED_IN]->(m:Movie{name:$movieName}) return n limit $limit;"
        elif genre == "DIRECTED_BY":
            sql = "match(m:Movie{name:$movieName})-[r:DIRECTED_BY]->(n:Director) return n limit $limit;"
        elif genre == "TYPE_OF":
            sql = "match(m:Movie{name:$movieName})-[r:TYPE_OF]->(n:Type) return n limit $limit;"
        else:
            return None
        resultList = self.queryNode(sql, movieName=movieName, genre=genre, limit=limit)
        return [result.get("n") for result in resultList]


if __name__ == '__main__':
    db = Neo4j("./DB.json")

    # sql = "match(n:Movie{name:$name}) return n limit 10;"
    # propertyDict = {"name": "The Matrix"}
    # results = db.query(sql, name="同级生 同級生")

    # results = db.queryMovieByName("同级生")
    results = db.queryMovieByType("剧情")
    print(type(results))
    print(results)

    db.close()
