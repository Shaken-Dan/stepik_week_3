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
    free = db.Column(db.String, nullable=False)
    booking = db.relationship("Booking", backref='teachers')

    def set_free_schedule(self, data):
        """Serialize and set the free schedule data."""
        self.free = json.dumps(data)

    def set_goals(self, data):
        self.goals = json.dumps(data)

    def get_free_schedule(self):
        """Deserialize and return the free schedule data as a dictionary."""
        return json.loads(self.free) if self.free else {}

    def get_goals(self):
        return json.loads(self.goals) if self.goals else {}


# One to mane relationship: Many bookings one teacher.
class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String, nullable=False)
    booked_time = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.Integer, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")


# with app.app_context():
#     with open("teacher_db.json", "r", encoding="utf-8") as file:
#         data_base = json.load(file)
#         name = data_base[0]['name']
#         about = data_base[0]['about']
#         rating = data_base[0]['rating']
#         picture = data_base[0]['picture']
#         price = data_base[0]['price']
#         goals = data_base[0]['goals']
#         free = data_base[0]['free']
#
#         # Check to avoid double name
#         if Teacher.query.filter_by(name=name).count() == 0:
#             teacher = Teacher(name=name, about=about, rating=rating, picture=picture, price=price, goals=goals,
#                               free=free)
#             teacher.set_goals(goals)
#             teacher.set_free_schedule(free)
#
#             db.session.add(teacher)
#             db.session.commit()
#         else:
#             print("Name already exists in data base")


with app.app_context():
    db.create_all()


