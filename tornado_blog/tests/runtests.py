
import unittest
import sys

TEST_MODULES = [
    'tests.models.model_test',
    'tests.controllers.controllers_test',
    'tests.handlers.handlers_test',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
   
    import tornado.testing
    
    tornado.testing.main()