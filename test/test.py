import unittest
import requests
import sys


PORT = 5001


def req(route, **args):
    r = requests.get('http://localhost:' + str(PORT) + "/" + route, params=args)
    return r.content, r.status_code


class Test(unittest.TestCase):

    def setUp(self):
        req('clear')

    def tearDown(self):
        req('clear')

    def test_clear(self):
        d, c = req('size')
        self.assertEqual(200, c)
        self.assertEqual(0, int(d))
        

if __name__ == "__main__":
    PORT = int(sys.argv[-1])
    sys.argv.pop()
    unittest.main()
