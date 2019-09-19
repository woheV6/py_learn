from src import app,db
import click
from src.models import Movie,User
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