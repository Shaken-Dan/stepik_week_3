import json

goal = "study"
with open("teacher_db.json", "r", encoding="utf-8") as file:
    data_base = json.load(file)
    # teacher_name = data_base[0]['name']
    for profile in data_base:
        if goal in profile['goals']:
            print(profile['id'])
