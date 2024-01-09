"""
Module for testing moo.  Folder structure, file name, and code 
are written to be compliant with python's unittest package, but 
main() can be called via importing
"""


import unittest 
from t3co import Global as gl


class TestMoo(unittest.TestCase):
    def test_moo(self):
        self.assertTrue(True) # TODO: actually build a test here

if __name__ == '__main__':
    unittest.main()