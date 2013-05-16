'''
Created on 16 May 2013

@author: Ali
'''
import unittest
from Views.mainPanel import formatMenuData

class Test(unittest.TestCase):
    def test_ExactSpacing(self):
        "Test case A"
        self.assertEqual(formatMenuData('a\tb\tc\td', 13, False), 'a   b   c   d', "Not spacing exact values correctly")
    
    def test_InexactSpacing(self):
        self.assertEqual(formatMenuData('a\tb\tc\td', 14, False), 'a   b   c    d', "Not spacing inexact values correctly - one fullsize")
        self.assertEqual(formatMenuData('a\tb\tc\td', 15, False), 'a   b    c    d', "Not spacing inexact values correctly - two fullsize")
    
    def test_Cutting(self):
        self.assertEqual(formatMenuData('test\ttest', 7, False), 'testtest', "Not spacing over-large values correctly")
        self.assertEqual(formatMenuData('test\ttest', 7, True), 'testtes', "Not cutting over-large values correctly")
    
    def test_SingleString(self):
        self.assertEqual(formatMenuData('test', 7, False), 'test   ', "Not handling no-split values correctly")
    
    def test_AlternateSeperator(self):
        self.assertEqual(formatMenuData('a|b|c|d', 13, False, '|'), 'a   b   c   d', "Not spacing exact values correctly with alternative seperator")
        self.assertEqual(formatMenuData('a|b|c|d', 14, False, '|'), 'a   b   c    d', "Not spacing inexact values correctly with alternative seperator - one fullsize")
        self.assertEqual(formatMenuData('a|b|c|d', 15, False, '|'), 'a   b    c    d', "Not spacing inexact values correctly with alternative seperator - two fullsize")
        
        self.assertEqual(formatMenuData('test|test', 7, False, '|'), 'testtest', "Not spacing over-large values correctly with alternative seperator")
        self.assertEqual(formatMenuData('test|test', 7, True, '|'), 'testtes', "Not cutting over-large values correctly with alternative seperator")
        
        self.assertEqual(formatMenuData('test', 7, False, '|'), 'test   ', "Not handling no-split values correctly with alternative seperator")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()