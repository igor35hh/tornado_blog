import tornado.web
import markdown
from app.basehandler.base_handler import BaseHandler
from app.controllers.compose_controller import ComposeController

class ComposeHandler(BaseHandler, ComposeController):
    
    @tornado.web.authenticated
    async def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = await self.get_entry_by_id(id)
        self.render("compose.html", entry=entry)
        
    
    @tornado.web.authenticated
    async def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        
        if id:
            entry = await self.get_entry_by_id(id)
            if not entry:
                raise tornado.web.HTTPError(404)
            
            await self.post_update_entry(title, text, html, id)
            
            self.redirect("/entry/" + entry['slug'])
            
        else:
            author_id = await self.current_user
            slug, entry_id = await self.post_new_entry(title, text, html, author_id)
            
            self.redirect("/entry/" + slug)
            