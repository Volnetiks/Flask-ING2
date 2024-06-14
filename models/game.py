class Game():
    id = ""
    name = ""
    category = ""
    year = 2000
    minPlayer = 1
    maxPlayer = 1
    age = 0
    length = ""
    user_id = ""
    favorite = False

    def __init__(self, id, name, year, minPlayer, maxPlayer, age, length, user_id, category, favorite=False) -> None:
        self.id = id
        self.name = name
        self.year = year
        self.minPlayer = minPlayer
        self.maxPlayer = maxPlayer
        self.age = age
        self.length = length
        self.user_id = user_id
        self.category = category
        self.favorite = favorite
