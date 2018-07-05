import tornado.web
from app.controllers.base_controller import BaseController
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

class BaseHandler(tornado.web.RequestHandler, BaseController):
    
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("blogdemo_user")
        if not user_id:
            return None
        return self.get_db_user(user_id)
    
    def set_secure_cookie(self, name, value, expires_days=30, version=None,
                          **kwargs):
        
        super(BaseHandler, self).set_secure_cookie(name, value, expires_days, version,
                          **kwargs)
        
        if self.application.save_cookies:
            self.application.cookies_ids[name] = value
            
    def get_secure_cookie(self, name, value=None, max_age_days=31,
                          min_version=None):
        
        user_id = super(BaseHandler, self).get_secure_cookie(name, value, max_age_days,
                          min_version)
        
        if self.application.save_cookies:
            if not user_id:
                user_id = self.application.cookies_ids.get(name)
                
        return user_id
        
    def clear_cookie(self, name, path="/", domain=None):
        
        super(BaseHandler, self).clear_cookie(name, path, domain)
        
        if self.application.save_cookies:
            self.application.cookies_ids = {}
            
    
