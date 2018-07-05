from app.controllers.base_controller import BaseController

class HomeController(BaseController):
    
    async def get_home_entries(self):
    
        entries = await self.db.select_all("SELECT * FROM entries ORDER BY published DESC LIMIT 5", ())
       
        return entries
        