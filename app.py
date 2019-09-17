from flask import Flask , render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
import click
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
app = Flask(__name__)

WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI']=prefix+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = '123456'
db= SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True) #主键
    username = db.Column(db.String(20))
    name = db.Column(db.String(20)) #名字
    password_hash = db.Column(db.String(128)) # hash散列值
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)
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

@app.cli.command()
@click.option('--username',prompt=True,help='The username to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create User"""
    db.create_all()
    user=User.query.first()
    if user is not None:
        click.echo('Updating user....')
        user.username=username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username,name='admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')
# 模版上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title=request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            flash('格式错误')
            return redirect(url_for('index'))
        movie = Movie(title=title,year=year)
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('电影创建成功')
        return redirect(url_for('index'))
    movies = Movie.query.all()
    return render_template('index.html',movies=movies)
@app.route('/user/<name>')
def user_name(name):
    return 'USer : %s' % name

@app.route('/test_url')
def testurl():
    print(url_for('hello'))
    print(url_for('user_name',name='zhangsan'))
    return 'test_url哈哈'
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404
@app.route('/movie/edit/<int:movie_id>',methods=["POST","GET"])
@login_required
def edit(movie_id):
    movie= Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title=request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            flash('格式错误')
            return redirect(url_for('edit',movie_id=movie_id))
        movie.title=title
        movie.year=year
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('edit',movie_id=movie_id))
    return render_template('edit.html',movie=movie)
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@login_manager.user_loader
def load_user(user_id):
    user= User.query.get(int(user_id))
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('登出')
    return redirect(url_for('index'))

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('setting'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('setting.html')
