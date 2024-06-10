from flask_login import UserMixin

class User(UserMixin):
    id = ""
    email = ""
    password = ""
    name = ""
    games = []
    admin = False

    def __init__(self, id, email, name, password, games = [], admin=False) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.games = games
        self.admin = admin