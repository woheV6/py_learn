from flask import Flask , render_template
from flask import url_for

from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

app = Flask(__name__)
WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI']=prefix+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db= SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) #主键
    name = db.Column(db.String(20)) #名字
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) #主键
    title = db.Column(db.String(20)) #电影标题
    year = db.Column(db.String(4)) # 电影年份

@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.') #设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') #输出提示信息


@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    name = "he hong"
    movies =[
        {"title":'放牛娃的春天','year':'2001'},
        {"title":'王二小','year':'1993'},
        {"title":'炮兵突击','year':'2003'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done')

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)
@app.route('/user/<name>')
def user_name(name):
    return 'USer : %s' % name

@app.route('/test_url')
def testurl():
    print(url_for('hello'))
    print(url_for('user_name',name='zhangsan'))
    return 'test_url哈哈'
