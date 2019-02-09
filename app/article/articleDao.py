from app.db.dao import MongoDAO


class ArticleDAO(MongoDAO):
    def __init__(self):
        MongoDAO.__init__(self, 'blog', 'article')
