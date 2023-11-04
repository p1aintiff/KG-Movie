from flask import Flask, render_template, request
from flask_cors import CORS
from database.OneMovie import movies

app = Flask(__name__)


# CORS(app, resources={r"/api/*": {"origins": "http://localhost:18098"}})


# 设置x-content-type-options头部
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    username = 'admin'
    if request.method == "POST":
        account = request.form['account']
        password = request.form['password']
        print(account, password)
        if account == 'admin' and password == '123456':
            return 'Login Success'

    return render_template('login.html', username=username)


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.method == "GET":
        return render_template('search.html')
    if request.method == "POST":
        searchType = request.form['searchType']
        query = request.form['query']

        if searchType == 'movie':
            movies.run(query)
            movieInfos = []
            movieInfos = movies.getMovieInfos()
            # print("flask", movieInfos)
            print(len(movieInfos))
        return render_template('result.html', datas=movieInfos)


if __name__ == '__main__':
    app.run(debug=True)
