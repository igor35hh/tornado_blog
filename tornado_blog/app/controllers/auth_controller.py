from tornado import gen
import bcrypt
from app.controllers.base_controller import BaseController
from app.basehandler.base_handler import executor

class AuthController(BaseController):
    
    async def post_auth_login(self, params):
        
        author = await self.db.select_one("SELECT * FROM authors WHERE email = %s", (params,))
        
        return author
    
    @gen.coroutine
    def check_password(self, password, author_hashed_password):
        
        hashed_password = yield executor.submit(
            bcrypt.hashpw, password.encode('utf8'), author_hashed_password.encode('utf8'))
        
        hashed_password = hashed_password.decode('utf8')
        
        if hashed_password == author_hashed_password:
            return True
        else:
            return False
    
    async def delete_author(self, email):
        
        await self.db.delete(
            "DELETE FROM authors WHERE email = %s"
            ,(email,))
        return True
    
    async def create_author(self, email, name, password):
        
        author = await self.post_auth_login(email)
        
        if author:
            return author['id']
        
        hashed_password = await self.create_password(password)
        
        author = await self.db.insert(
            "INSERT INTO authors (email, name, hashed_password) VALUES (%s, %s, %s) RETURNING id",
            (email, name, hashed_password,))
        
        return author['id']
    
    @gen.coroutine
    def create_password(self, password):
        
        hashed_password = yield executor.submit(
            bcrypt.hashpw, password.encode('utf8'),
            bcrypt.gensalt())
        
        hashed_password = hashed_password.decode('utf8')
        
        return hashed_password
