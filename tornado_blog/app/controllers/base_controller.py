
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)
    
class BaseController():
    
    async def get_db_user(self, user_id):
        author = await self.db.select_one("SELECT * FROM authors WHERE id = %s", (int(user_id),))
        user_id = author.get('id', None)
        return user_id
    
    async def any_author_exists(self): 
        cursor = await self.db.select_one("SELECT * FROM authors LIMIT 1", ())
        return bool(cursor)