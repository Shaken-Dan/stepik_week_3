import json


class JsonTeachers:
    def __init__(self, id):
        with open("teacher_db.json", "r", encoding="utf-8") as file:
            data_base = json.load(file)
            info = data_base[id]
            self.name = data_base[id]['name']
            self.about = data_base[id]['about']
            self.rating = data_base[id]['rating']
            self.picture = data_base[id]['picture']
            self.price = data_base[id]['price']
            self.goals = data_base[id]['goals']
            self.free = data_base[id]['free']


result = JsonTeachers(1)
print(result.name)
