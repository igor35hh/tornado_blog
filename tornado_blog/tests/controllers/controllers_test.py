from ..base_test import BaseTest, gen_test

from app.controllers.base_controller import BaseController
from app.controllers.home_controller import HomeController
from app.controllers.entry_controller import EntryController
from app.controllers.archive_controller import ArchiveController
from app.controllers.auth_controller import AuthController
from app.controllers.compose_controller import ComposeController

class BaseControllersTest(BaseTest, BaseController):
    
    @property
    def db(self):
        return self.get_app().db
    
    @gen_test
    async def test_get_user(self):
        user = await self.get_db_user(0)
        self.assertTrue(user or user == None)
        
    @gen_test
    async def test_any_author_exists(self):
        user = await self.any_author_exists()
        self.assertTrue(user or user == False)

class HomeControllerTest(BaseControllersTest, HomeController):
    
    @gen_test
    async def test_get_entries(self):
        entries = await self.get_home_entries()
        self.assertTrue(isinstance(entries, list))
        
class EntryControllerTest(BaseControllersTest, EntryController):
    
    @gen_test
    async def test_get_entries(self):
        entries = await self.get_entry_entries('slug')
        self.assertTrue(isinstance(entries, dict))
        
class ArchiveControllerTest(BaseControllersTest, ArchiveController):
    
    @gen_test
    async def test_get_archive_entries(self):
        entries = await self.get_archive_entries()
        self.assertTrue(isinstance(entries, list))
        
class AuthControllerTest(BaseControllersTest, AuthController):
    
    @gen_test
    async def test_create_author(self):
        author = await self.create_author('email@ua.fm', 'Test name', '123')
        self.assertTrue(author)
        
    @gen_test
    async def test_create_password(self):
        res = await self.create_password('123')
        self.assertTrue(res)
        
    @gen_test
    async def test_delete_author(self):
        res = await self.delete_author('email@ua.fm')
        self.assertTrue(res)
        
    @gen_test
    async def test_post_auth_login(self):
        entries = await self.post_auth_login('email@ua.fm')
        self.assertTrue(isinstance(entries, dict))
        
    @gen_test
    async def test_check_password(self):
        res = await self.check_password('123', '$2b$12$RwYOf7KPAFY8IjN0OihIouwznCGy1aSQ.0mbqfIr.GdXZgfblSHtO')
        self.assertTrue(res)
        
        res = await self.check_password('1234', '$2b$12$RwYOf7KPAFY8IjN0OihIouwznCGy1aSQ.0mbqfIr.GdXZgfblSHtO')
        self.assertFalse(res)
        
class ComposeControllerTest(ComposeController, AuthControllerTest):
    
    @gen_test
    async def test_get_entry_by_id(self):
        entries = await self.get_entry_by_id(0)
        self.assertTrue(isinstance(entries, dict))
        
    @gen_test
    async def test_get_entry_by_slug(self):
        entries = await self.get_entry_by_slug('slug')
        self.assertTrue(isinstance(entries, dict))
        
    @gen_test
    async def test_post_new_entry(self):
        
        author = await self.create_author('email@ua.fm', 'Test name', '123')
        self.assertTrue(author)
        
        slug, entry_id = await self.post_new_entry('title', 'text', 'html', author)
        self.assertTrue('title' in slug)
        
        res = await self.post_update_entry('title', 'text', 'html', entry_id)
        self.assertTrue(res)
        
        res = await self.delete_entry_by_id(entry_id)
        self.assertTrue(res)
        
        res = await self.delete_author('email@ua.fm')
        self.assertTrue(res)
        
        
    
        
    

        
        
        