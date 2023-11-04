## 电影图数据库

数据来源某网站，侵删

## 快速开始

### 1. 安装依赖

在项目根目录Knowledge-Graph下执行

```bash
pip install -r requirements.txt
```

### 2. 配置数据库文件

在database目录下创建`DB.json`文件， 写入以下内容  
值需要根据自己的数据库配置进行修改，写在`""`中

```json
{
  "URI": "bolt://localhost:7687",
  "USER": "neo4j",
  "PASSWORD": ""
}
```

### 3.运行app.py

在webServer目录下执行

```bash
python app.py
```

或者
在编译器中运行app.py

<hr>

## 项目结构

主要结构
```
Knowledge-Graph
├── database
│   ├── DB.json # 数据库配置文件
│   ├── DBneo4j.py # neo4j数据库操作
│   ├── OneMovie.py # 查询电影的类

├── webServer # web服务 使用flask
│   ├── app.py # web服务入口
│   ├── static # 静态文件
│   └── templates # 模板文件
│       ├── index.html # 主页
│       ├── result.html # 查询结果模板
│       └── search.html # 查询页面
├── README.md
├── requirements.txt # 依赖
└── douban # 爬虫部分，可以忽略
```


