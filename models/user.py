import json
from flask_login import UserMixin

class User(UserMixin):
    id = ""
    email = ""
    password = ""
    name = ""
    games = []

    def __init__(self, id, email, name, password, games = []) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.games = games


    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)