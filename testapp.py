# -*- coding: utf-8 -*
from app import app,db,Movie,User
import unittest
class AppTestCase(unittest.TestCase):
    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING = True,
            SQLALCHEMY_DATABASE_URI='sqlite:///memory:'
        )
        # 创建数据库和表
        db.create_all()
        user = User(name='Test',username='test')
        user.set_password('123')
        movie =  Movie(title='ui',year='2018')
        db.session.add_all([user,movie])
        db.session.commit()
        self.client=app.test_client()
        self.runner=app.test_cli_runner()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    def test_app_exist(self):
        self.assertIsNotNone(app)
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
if __name__ == '__main__':
    unittest.main()