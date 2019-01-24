# user: login_require
# all: vistor
# owner: owner_only

Policy = {
    'article': {
        'GET': "all",
        'PUT': "owner",
        'DELETE': "owner"
    },
    "users": {
        'GET': "all",
        'PUT': "owner",
        'DELETE': "owner"
    },
    "login":{
        'POST': 'all',
        'GET': 'owner'
    }
}
