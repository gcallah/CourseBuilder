import unittest
from url_checker import OurHTMLParser

class TestUrlChecker(unittest.TestCase):
    '''
    Tests for url_checker.py
    '''
    def setUp(self):
        self.url_checker = OurHTMLParser()

    def test_valid_url(self):
        link1 = "https://www.arrestedcoursebuilder.com/"
        link2 = "http://coursebuildercafe.org/"
        self.assertTrue(self.url_checker.is_accessible(link1))
        self.assertTrue(self.url_checker.is_accessible(link2))

    def test_invalid_url(self):
        link2 = "weird.link.org"
        self.assertFalse(self.url_checker.is_accessible(link2))

if __name__ == '__main__':
    unittest.main()
