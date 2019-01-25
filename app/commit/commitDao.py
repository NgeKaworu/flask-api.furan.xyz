from app.db.dao import MongoDAO


class CommitDAO(MongoDAO):
    def __init__(self):
        MongoDAO.__init__(self, 'commit', 'commit')
