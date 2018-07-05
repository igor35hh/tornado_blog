from ..base_test import BaseTest, gen_test
from urllib.parse import urlencode
import re

class HomePageHandlerTest(BaseTest):
    
    def test_home_page_exist(self):
        resp = self.fetch('/', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'Sign in</a>', resp.body)
        
class AuthCreatePageHandlerTest(BaseTest):
    
    def test_login_create_page_exist(self):
        resp = self.fetch('/auth/create', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>New author:)</h4>', resp.body)
        self.assertIn(b'name="name"', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
     
class AuthComposeTest(BaseTest):
    
    def test_create_login(self):
        resp = self.fetch('/auth/create', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>New author:)</h4>', resp.body)
        self.assertIn(b'name="name"', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'name':'Test name', 'email': 'email@ua.fm','password': 123, '_xsrf': _xsrf}
        body = urlencode(data)
        
        resp = self.fetch('/auth/create', method='POST', headers={'Cookie': resp.headers['Set-Cookie']}, body=body, follow_redirects=False)
        self.assertEqual(resp.code, 302)
    
        resp = self.fetch('/', method='GET', headers={'Cookie':resp.headers['Set-Cookie']})
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'<a href="/compose">New post</a>', resp.body)
        self.assertIn(b'Sign out', resp.body)
    
    def test_wrong_login(self):
        resp = self.fetch('/auth/login', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>Please sign in</h4>', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'email': 'email@ua.fm','password': 1234, '_xsrf': _xsrf}
        body = urlencode(data)
        
        resp = self.fetch('/auth/login', method='POST', headers={'Cookie': resp.headers['Set-Cookie']}, body=body, follow_redirects=False)
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<span style="color: red">Error: incorrect password</span>', resp.body)
        self.assertIn(b'<h4>Please sign in</h4>', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
    def test_wrong_author(self):
        resp = self.fetch('/auth/login', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>Please sign in</h4>', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'email': '1email@ua.fm','password': 123, '_xsrf': _xsrf}
        body = urlencode(data)
        
        resp = self.fetch('/auth/login', method='POST', headers={'Cookie': resp.headers['Set-Cookie']}, body=body, follow_redirects=True)
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>New author:)</h4>', resp.body)
        self.assertIn(b'name="name"', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
            
    def test_login_logout(self):
        
        resp = self.fetch('/auth/login', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>Please sign in</h4>', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'email': 'email@ua.fm','password': 123, '_xsrf': _xsrf}
        body = urlencode(data)
        
        resp = self.fetch('/auth/login', method='POST', headers={'Cookie': resp.headers['Set-Cookie']}, body=body, follow_redirects=False)
        self.assertEqual(resp.code, 302)
    
        resp = self.fetch('/', method='GET', headers={'Cookie':resp.headers['Set-Cookie']})
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'<a href="/compose">New post</a>', resp.body)
        self.assertIn(b'<a href="/auth/logout?next=%2F">Sign out</a>', resp.body)
        
        resp = self.fetch('/auth/logout', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'<a href="/auth/login?next=%2F">Sign in</a>', resp.body)
        
    def test_create_new_entry(self):
        
        resp = self.fetch('/auth/login', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>Please sign in</h4>', resp.body)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'email': 'email@ua.fm','password': 123, '_xsrf': _xsrf}
        body = urlencode(data)
        
        headers={'Cookie': resp.headers['Set-Cookie']}
        resp = self.fetch('/auth/login', method='POST', headers=headers, body=body, follow_redirects=False)
        self.assertEqual(resp.code, 302)
        
        headers={'Cookie': resp.headers['Set-Cookie']}
        resp = self.fetch('/compose', method='GET', headers=headers)
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/compose">New post</a>', resp.body)
        self.assertIn(b'<a href="/auth/logout?next=%2Fcompose">Sign out</a>', resp.body)
        self.assertIn(b'<h4>Leave a Post:</h4>', resp.body)
        self.assertIn(b'name="title"', resp.body)
        self.assertIn(b'name="markdown"', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        data = {'title': 'test post test','markdown': 'ahahahahahahahahah', '_xsrf': _xsrf}
        body = urlencode(data)
        
        headers={'Cookie': resp.headers['Set-Cookie']}
        resp = self.fetch('/compose', method='POST', headers=headers, body=body, follow_redirects=True)
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'<p>ahahahahahahahahah</p>', resp.body)
        self.assertIn(b'/compose?id=', resp.body)
        
        m1 = re.search(r'href="/compose+[^"]+"', resp.body.decode()).group()
        compose_link = m1.replace('href="','').replace('"','')
        
        m1 = re.search(r'<a href="[^"]+">test post test</a>', resp.body.decode()).group()
        entry_link = m1.replace('<a href="','').replace('">test post test</a>','')
        
        resp = self.fetch(entry_link, method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'%s' % entry_link.encode(), resp.body)
        self.assertIn(b'test post test', resp.body)
        
        resp = self.fetch(compose_link, method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<h4>Change a Post:</h4>', resp.body)
        self.assertIn(b'action="/compose"', resp.body)
        self.assertIn(b'value="test post test"', resp.body)
        self.assertIn(b'ahahahahahahahahah</textarea>', resp.body)
        
        _xsrf = self.get_xsrf_key(resp.body.decode())
        
        m1 = re.search(r'name="id" value="[\d]+', resp.body.decode()).group()
        id_compose = m1.replace('name="id" value="','')
        
        data = {'id': id_compose, 'title': 'test post test','markdown': 'ohohohohohohoho', '_xsrf': _xsrf}
        body = urlencode(data)
        
        headers={'Cookie': resp.headers['Set-Cookie']}
        resp = self.fetch('/compose', method='POST', headers=headers, body=body, follow_redirects=True)
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        self.assertIn(b'<p>ohohohohohohoho</p>', resp.body)
        
        resp = self.fetch('/auth/logout', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        
        #print(resp)
        #print(resp.body)
        
class AuthLoginPageHandlerTest(BaseTest):
    
    def test_login_page_exist(self):
        resp = self.fetch('/auth/login', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'name="email"', resp.body)
        self.assertIn(b'name="password"', resp.body)
        
class LogoutPageHandlerTest(BaseTest):
    
    def test_logout_page_exist(self):
        resp = self.fetch('/auth/logout', method='GET')
        self.assertEqual(resp.code, 200)
        self.assertIn(b'<a href="/">Home</a>', resp.body)
        
class ComposePageHandlerTest(BaseTest):
    
    def test_compose_page_exist(self):
        resp = self.fetch('/compose', method='GET')
        self.assertEqual(resp.code, 200)

class ArchivePageHandlerTest(BaseTest):
    
    def test_archive_page_exist(self):
        resp = self.fetch('/archive', method='GET')
        self.assertEqual(resp.code, 200)
        
        
        
    
            
    
        
