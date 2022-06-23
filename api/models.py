class User:
    def __init__(self, index, username, uuid, password, salt, date_created):
        self.index = index
        self.username = username
        self.uuid = uuid
        self.password = password
        self.salt = salt
        self.date_created = date_created
        self.date_modified = ""


class Todo:
    def __init__(self, index, belongs_to, body, done, date_created):
        self.index = index
        self.belongs_to = belongs_to
        self.body = body
        self.done = done
        self.date_created = date_created
        self.date_modified = ""
