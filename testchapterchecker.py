import unittest
from chapterchecker import *
from mock import MagicMock

class ChapterChecker(unittest.TestCase):   
    def test_canary(self):
        self.assertTrue(True)   
        
    def test_story_page_exists(self):
        status_mock = MagicMock()
        status_mock.__xpath__.return_value = [1]
        
        self.assertTrue(story_page_exists("http://www.google.com"))        
        
if __name__ == '__main__':
    unittest.main()