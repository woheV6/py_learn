from src import app,db
from src.models import Movie,User
from flask_login import login_required,LoginManager
from flask import render_template,request,url_for,redirect,flash

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
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('setting.html')