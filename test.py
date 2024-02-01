import json
from random import sample
with open("teacher_db.json", "r", encoding="utf-8") as file:
    data_base = json.load(file)
    random_profiles = sample(data_base, 6)
    for profile in random_profiles:
        print(profile['name'])

