
import unicodedata
import re, random
from app.controllers.base_controller import BaseController

class ComposeController(BaseController):
    
    async def get_entry_by_id(self, id):
        entry = await self.db.select_one("SELECT * FROM entries WHERE id = %s", (int(id),))
        return entry
    
    async def get_entry_by_slug(self, slug):
        entry = await self.db.select_one("SELECT * FROM entries WHERE slug = %s", (slug,))
        return entry
    
    async def post_update_entry(self, title, text, html, id):
        await self.db.update(
                "UPDATE entries SET updated = now(), title = %s, markdown = %s, html = %s WHERE id = %s", (title, text, html, int(id),))
        return True    
            
    async def post_new_entry(self, title, text, html, author_id):
        slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
        slug = re.sub(r"[^\w]+", " ", slug.decode())
        slug = "-".join(slug.lower().strip().split())
        if not slug:
            slug = "entry"
            
        slug += "-"+str(random.randint(1, 1000))
        
        entry = await self.db.insert(
                "INSERT INTO entries (author_id,title,slug,markdown,html,published,updated) VALUES (%s,%s,%s,%s,%s,now(),now()) RETURNING id", 
               (author_id, title, slug, text, html,))
        
        return slug, entry['id']
    
    async def delete_entry_by_id(self, id):
        await self.db.delete(
            "DELETE FROM entries WHERE id = %s"
            , (int(id),))
        return True
    
       
    
    
        