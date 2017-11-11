import unittest
import requests
import sys


PORT = 5001


def req(route, **args):
    r = requests.get('http://localhost:' + str(PORT) + "/" + route, params=args)
    return r.content.decode('utf-8'), r.status_code


class Test(unittest.TestCase):

    def setUp(self):
        _, c = req('clear')
        self.assertEqual(200, c)

    def tearDown(self):
        _, c = req('clear')
        self.assertEqual(200, c)

    def test_zero_size_at_start(self):
        d, c = req('size')
        self.assertEqual((0, 200), (int(d), c))

    def test_put(self):
        _, c = req('put', k='wang', v='guan')
        self.assertEqual(200, c)
        d, c = req('size')
        self.assertEqual((1, 200), (int(d), c))
        d, c = req('put', k='wang', v='guan')
        self.assertEqual(("guan", 205), (d, c))
        d, c = req('size')
        self.assertEqual((1, 200), (int(d), c))

    def test_put_bad_request(self):
        _, c = req('put', k='wang')
        self.assertEqual(400, c)
        _, c = req('put', v='guan')
        self.assertEqual(400, c)
        _, c = req('put')
        self.assertEqual(400, c)

    def test_get(self):
        _, c = req('get', k="wang")
        self.assertEqual(204, c)
        _, c = req('get', i="0")
        self.assertEqual(204, c)
        req('put', k='wang', v='guan')
        d, c = req('get', k="wang")
        self.assertEqual(("guan", 200), (d, c))
        d, c = req('get', i="0")
        self.assertEqual(("wang", 200), (d, c))

    def test_get_bad_request(self):
        _, c = req('get')
        self.assertEqual(400, c)
        _, c = req('get', i="not_int")
        self.assertEqual(400, c)

    def test_remove(self):
        _, c = req('remove', k="wang")
        self.assertEqual(204, c)
        req('put', k='wang', v='guan')
        d, c = req('size')
        self.assertEqual((1, 200), (int(d), c))
        d, c = req('remove', k="wang")
        self.assertEqual(("guan", 200), (d, c))
        d, c = req('size')
        self.assertEqual((0, 200), (int(d), c))

    def test_remove_bad_request(self):
        _, c = req('remove')
        self.assertEqual(400, c)

    def test_clear(self):
        _, c = req('clear')
        self.assertEqual(200, c)
        d, c = req('size')
        self.assertEqual((0, 200), (int(d), c))
        req('put', k='wang', v='guan')
        d, c = req('size')
        self.assertEqual((1, 200), (int(d), c))
        req('put', k='blume', v='christian')
        d, c = req('size')
        self.assertEqual((2, 200), (int(d), c))
        _, c = req('clear')
        self.assertEqual(200, c)
        d, c = req('size')
        self.assertEqual((0, 200), (int(d), c))

    def test_put_get_unicode(self):
        _, c = req('put', k='wang', v='güan')
        self.assertEqual(200, c)
        d, c = req('get', k="wang")
        self.assertEqual(("güan", 200), (d, c))


if __name__ == "__main__":
    PORT = int(sys.argv[-1])
    sys.argv.pop()
    unittest.main()
