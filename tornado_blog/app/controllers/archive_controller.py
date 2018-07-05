from app.controllers.base_controller import BaseController

class ArchiveController(BaseController):
    
    async def get_archive_entries(self):
    
        entries = await self.db.select_all("SELECT * FROM entries ORDER BY published DESC", ())
       
        return entries