# user: login_require
# all: vistor
# owner: owner_only

Policy = {
    'article': {
        'GET': "all",
        'PUT': "owner",
        'DELETE': "owner",
        'POST': 'admin'
    },
    'articles': {
        'GET': "all",
        'POST': "admin"
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
        'POST': 'admin',
        'GET': 'all'
    }
}
