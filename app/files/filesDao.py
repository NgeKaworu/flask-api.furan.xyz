from app.db.dao import MongoDAO


class FilesDAO(MongoDAO):
    def __init__(self):
        MongoDAO.__init__(self, 'blog', 'files')
