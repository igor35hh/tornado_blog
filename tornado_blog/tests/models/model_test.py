
from ..base_test import BaseTest, gen_test

from app.model.model import ModelCRUD

class ModelTest(BaseTest):
    
    def test_if_class_exist(self):
        self.assertFalse(self.get_app().db is None)
        self.assertTrue(isinstance(self.get_app().db, ModelCRUD))
    
    @gen_test
    async def test_if_tables_exist(self):
        entry = await self.get_app().db.select_one(
            "SELECT EXISTS (SELECT 1 FROM   information_schema.tables WHERE  table_name = 'authors')"
            , ())
        self.assertTrue(entry['exists'])
        
        entry = await self.get_app().db.select_one(
            "SELECT EXISTS (SELECT 1 FROM   information_schema.tables WHERE  table_name = 'entries')"
            , ())
        self.assertTrue(entry['exists'])
        
    @gen_test
    async def test_crud_operations(self):
        
        await self.get_app().db.delete(
            "DELETE FROM authors WHERE email = %s",
            ('email@ua.fm',))
        
        #insert, select
        new_author = await self.get_app().db.insert(
            "INSERT INTO authors (email, name, hashed_password) VALUES (%s, %s, %s) RETURNING id"
            ,('email@ua.fm', 'Test name', 'hashed_password',))
        
        author = await self.get_app().db.select_one(
            "SELECT * FROM authors WHERE id = %s"
            , (new_author['id'],))
        self.assertTrue(new_author['id'] == author['id'])
        
        #update, select all
        await self.get_app().db.update(
            "UPDATE authors SET name = %s WHERE id = %s"
            ,('Test name new', author['id'],))
        
        author = await self.get_app().db.select_all(
            "SELECT * FROM authors WHERE id = %s"
            , (new_author['id'],))
        self.assertTrue(author[0]['name'] == 'Test name new')
        
        #delete, select
        await self.get_app().db.delete(
            "DELETE FROM authors WHERE email = %s",
            ('email@ua.fm',))
        
        author = await self.get_app().db.select_one(
            "SELECT * FROM authors WHERE email = %s"
            , ('email@ua.fm',))
        self.assertFalse(author)
        
        
        
    
        
        
    