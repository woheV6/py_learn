from flask import Flask , render_template
from flask import url_for
app = Flask(__name__)
name = 'he hong'
movies=[
    {'title':'美国队长','year':2018},
    {'title':'士兵突击','year':2008},
]
@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)
@app.route('/user/<name>')
def user_name(name):
    return 'USer : %s' % name

@app.route('/test_url')
def testurl():
    print(url_for('hello'))
    print(url_for('user_name',name='zhangsan'))
    return 'test_url哈哈'