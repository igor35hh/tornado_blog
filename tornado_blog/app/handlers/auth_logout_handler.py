from app.basehandler.base_handler import BaseHandler
from app.controllers.base_controller import BaseController

class AuthLogoutHandler(BaseHandler, BaseController):
    def get(self):
        self.clear_cookie("blogdemo_user")
        self.redirect(self.get_argument("next", "/"))