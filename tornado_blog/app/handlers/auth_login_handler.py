from app.basehandler.base_handler import BaseHandler
from app.controllers.auth_controller import AuthController

class AuthLoginHandler(BaseHandler, AuthController):
    
    async def get(self):
        if not await self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)
            
    async def post(self):
        author = await self.post_auth_login(self.get_argument("email"))
        
        if not author:
            self.redirect("/auth/create")
            return
        
        res = await self.check_password(self.get_argument("password"), author['hashed_password'])
        
        if res:
            self.set_secure_cookie("blogdemo_user", str(author['id']))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")
            