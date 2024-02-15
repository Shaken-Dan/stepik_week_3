from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'test_teacher.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    goals = db.Column(db.String, nullable=False)
    # How to write to a data-base?
    free_schedule = db.Column(db.String, nullable=False)

    def set_free_schedule(self, data):
        """Serialize and set the free schedule data."""
        self.free_schedule = json.dumps(data)

    def set_goals(self, data):
        self.goals = json.dumps(data)

    def get_free_schedule(self):
        """Deserialize and return the free schedule data as a dictionary."""
        return json.loads(self.free_schedule) if self.free_schedule else {}

    def get_goals(self):
        return json.loads(self.goals) if self.goals else {}


def is_name_unique():
    pass


with app.app_context():
    with open("teacher_db.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        name = data_base[0]['name']
        about = data_base[0]['about']
        rating = data_base[0]['rating']
        picture = data_base[0]['picture']
        price = data_base[0]['price']
        goals = data_base[0]['goals']
        free = data_base[0]['free']

        teacher = Teacher(name=name, about=about, rating=rating, picture=picture, price=price, free_schedule=free)
        teacher.set_goals(goals)
        teacher.set_free_schedule(free)
        db.session.add(teacher)
        db.session.commit()

        # teacher_to_delete = Teacher.query.filter_by(name="Morris Simmmons").first()
        #
        # if teacher_to_delete:
        #     db.session.delete(teacher_to_delete)
        #     db.session.commit()
        #     print("Teacher deleted")
        # else:
        #     print("Teacher not exists")


# if __name__ == "__main__":
#     app.run(debug=True)
