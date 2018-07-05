from app.controllers.base_controller import BaseController

class EntryController(BaseController):
    
    async def get_entry_entries(self, params):
        
        entries = await self.db.select_one("SELECT * FROM entries WHERE slug = %s", (params,))
       
        return entries