from sayhello import sayhello
import unittest
class SayHelloTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_say_hello(self):
        rv = sayhello()
        self.assertEqual(rv,'Hello!')
    def test_sayhello_somebody(self):
        rv = sayhello(to='he')
        self.assertEqual(rv,'Hello, he!')
if __name__ == '__main__':
    unittest.main()
