import tornado.web
from app.basehandler.base_handler import BaseHandler
from app.controllers.entry_controller import EntryController

class EntryHandler(BaseHandler, EntryController):
    
    async def get(self, slug):
        entry = await self.get_entry_entries(slug)
        
        if not entry:
            raise tornado.web.HTTPError(404)
        
        self.render("entry.html", entry=entry)