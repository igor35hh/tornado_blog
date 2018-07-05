import momoko
from tornado import gen

class ModelCRUD():
    
    def __init__(self, options, ioloop):
        
        self.db = momoko.Pool(
            dsn='dbname=%s user=%s password=%s host=%s port=%s' % (
                options.psql_database,
                options.psql_user,
                options.psql_password,
                options.psql_host,
                options.psql_port,
            ),
            size=1,
            ioloop=ioloop,
        )
        
    @property
    def get_db(self):
        return self.db
    
    @gen.coroutine
    def update(self, query, params):
        yield self.db.execute(query, params)
        
    @gen.coroutine
    def insert(self, query, params):
        cursor = yield self.db.execute(query, params)
        cursor_one = cursor.fetchone()
        cursor_desc = cursor.description
        if cursor_one:
            entry = dict(zip(list(zip(*cursor_desc))[0], cursor_one))
        else:
            entry = {}
        return entry
        
    @gen.coroutine
    def delete(self, query, params):
        yield self.db.execute(query, params)
        
    @gen.coroutine
    def select_one(self, query, params):
        cursor = yield self.db.execute(query, params)
        cursor_one = cursor.fetchone()
        cursor_desc = cursor.description
        if cursor_one:
            entry = dict(zip(list(zip(*cursor_desc))[0], cursor_one))
        else:
            entry = {}
        return entry
    
    @gen.coroutine
    def select_all(self, query, params):
        cursor = yield self.db.execute(query, params)
        cursor_all = cursor.fetchall()
        cursor_desc = cursor.description
        if cursor_all:
            entries = [dict(zip(list(zip(*cursor_desc))[0], row)) for row in cursor_all]
        else:
            entries = []
        return entries

    
    
    