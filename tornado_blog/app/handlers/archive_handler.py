from app.basehandler.base_handler import BaseHandler
from app.controllers.archive_controller import ArchiveController

class ArchiveHandler(BaseHandler, ArchiveController):
    
    async def get(self):
        entries = await self.get_archive_entries()
        
        self.render("archive.html", entries=entries)