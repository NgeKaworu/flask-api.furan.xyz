from app.db.dao import MongoDAO


class UsersDAO(MongoDAO):
    def __init__(self):
        MongoDAO.__init__(self, 'users', 'users')
