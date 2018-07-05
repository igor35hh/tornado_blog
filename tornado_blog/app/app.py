import tornado.web
import os
from pathlib import Path

from .handlers.home_handler import HomeHandler
from .handlers.archive_handler import ArchiveHandler
from .handlers.compose_handler import ComposeHandler
from .handlers.entry_handler import EntryHandler
from .handlers.auth_create_handler import AuthCreateHandler
from .handlers.auth_login_handler import AuthLoginHandler
from .handlers.auth_logout_handler import AuthLogoutHandler

from .handlers.entry_module import EntryModule

#wnnew@ua.fm 123

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/archive", ArchiveHandler),
            (r"/compose", ComposeHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/auth/create", AuthCreateHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        
        parent_path = str(Path(__file__).resolve().parent.parent)
        
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(parent_path, "templates"),
            static_path=os.path.join(parent_path, "static"),
            ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="asdfasdf",
            login_url="/auth/login",
            debug=True,
        )
        
        super(Application, self).__init__(handlers, **settings)
        
        self.db = None
        self.cookies_ids = {}
        self.save_cookies = False
        
        