import json
from data import teachers

with open("teacher_db.json", "w", encoding="utf-8") as f:
    json.dump(teachers, f, indent=4, ensure_ascii=False)
