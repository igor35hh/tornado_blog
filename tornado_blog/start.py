from tornado.options import define, options
import tornado.web
from app.app import Application
from app.model.model import ModelCRUD

define("port", default=8888, help="run on the given port", type=int)
define("psql_host", default="127.0.0.1", help="blog database host")
define("psql_port", default="5432", help="blog database host")
define("psql_database", default="tornado_blog", help="blog database name")
define("psql_user", default="igor", help="blog database user")
define("psql_password", default="", help="blog database password")

def create_app():
    
    application = Application()
    ioloop = tornado.ioloop.IOLoop.instance()
    
    application.db = ModelCRUD(options, ioloop)
    
    future = application.db.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()
    
    return application, ioloop
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application, ioloop = create_app()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    ioloop.start()
    