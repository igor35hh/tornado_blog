
from app.basehandler.base_handler import BaseHandler
from app.controllers.home_controller import HomeController

class HomeHandler(BaseHandler, HomeController):
    
    async def get(self):
        
        entries = await self.get_home_entries()
    
        if not entries:
            self.redirect("/compose")
            return
        self.render("home.html", entries=entries)