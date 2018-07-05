
from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.web
import re

from start import create_app

application, ioloop = create_app()

class BaseTest(AsyncHTTPTestCase):
        
    def setUp(self):
        super(BaseTest, self).setUp()
        self.get_app().save_cookies = True
        
    def get_app(self):
        return application
    
    def get_new_ioloop(self):
        return ioloop
    
    def get_xsrf_key(self, cookie):
        m1 = re.search(r'name="_xsrf" value="+[^"]+', cookie).group()
        _xsrf = m1.replace('name="_xsrf" value="','')
        return _xsrf
    
    def tearDown(self):
        pass
    
    def test_app_exists(self):
        self.assertFalse(application is None)
        
    @gen_test
    def test_clear_tables(self):
        yield self.get_app().db.delete("TRUNCATE authors, entries", ())
        
        

