# user: login_require
# all: vistor
# owner: owner_only

Policy = {
    'article': {
        'GET': "all",
        'PUT': "owner",
        'DELETE': "owner",
        'POST': 'user'
    },
    'articles': {
        'GET': "all",
        'POST': "user"
    },
    "users": {
        'GET': "all",
        'PUT': "owner",
        'DELETE': "owner"
    },
    "login": {
        'POST': 'all',
        'GET': 'owner'
    },
    "files": {
        'POST': 'user',
        'GET': 'all'
    }
}
