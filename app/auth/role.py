USER = 1
ADMIN = 2
VISITOR = 3

Role = {
    USER: {
        "user": {"POST": True, "PATCH": True, "GET": True, "DELETE": True},
        "share": {"POST": True}
    },
    ADMIN: {
        "user": {"POST": True, "PATCH": True, "GET": True, "DELETE": True},
        "share": {"POST": True}
    },
    VISITOR: {
        "user": {"GET": True}
    }
}