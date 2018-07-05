
from app.basehandler.base_handler import BaseHandler
from app.controllers.auth_controller import AuthController

class AuthCreateHandler(BaseHandler, AuthController):
    
    def get(self):
        self.render("create_author.html")
        
    async def post(self):
        
        author_id = await self.create_author(
            self.get_argument("email"), self.get_argument("name"), self.get_argument("password"))
        
        self.set_secure_cookie("blogdemo_user", str(author_id))
        self.redirect(self.get_argument("next", "/"))