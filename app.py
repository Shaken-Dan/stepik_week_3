import json
import os
from flask import Flask, render_template, abort, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired
from random import sample
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "afasfasfaf848a4sf8as41f5a1sf15"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'test_teacher.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

days = {'mon': 'Понедельник',
        'tue': "Persembe",
        'wed': "Среда",
        'thu': "Четверг",
        'fri': "Жұма",
        'sat': "Сенбі",
        'sun': "Воскресенье"
        }


# Reading teacher_db.json data for teachers
class JsonTeachers:
    def __init__(self, id):
        with open("teacher_db.json", "r", encoding="utf-8") as file:
            data_base = json.load(file)
            self.name = data_base[id]['name']
            self.about = data_base[id]['about']
            self.rating = data_base[id]['rating']
            self.picture = data_base[id]['picture']
            self.price = data_base[id]['price']
            self.goals = data_base[id]['goals']
            self.free = data_base[id]['free']


# Teacher DataBase Model
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


class UserForm(FlaskForm):
    clientName = StringField("Вас зовут")
    clientPhone = IntegerField("Ваш телефон")
    submit = SubmitField("Записаться на пробный урок")
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()


class RequestForm(FlaskForm):
    objective = RadioField(
        'travel',
        choices=[('goal1', 'Для путешествий'), ('goal2', 'Для школы'), ('goal3', 'Для работы'),
                 ('goal4', 'Для переезда')],
        validators=[DataRequired()])
    time_budget = RadioField(
        'time',
        choices=[('time1', '1-2 часа в неделю'), ('time2', '3-5 часов в неделю'), ('time3', '5-7 часов в неделю'),
                 ('time4', '7-10 часов в неделю')],
        validators=[DataRequired()])
    name = StringField("Вас зовут", validators=[DataRequired()])
    phone = IntegerField("Ваш телефон", validators=[DataRequired()])


@app.route('/')
def index():
    with open("teacher_db.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        random_profiles = sample(data_base, 6)
    return render_template('index.html', profiles=random_profiles)


# Все репетиторы
@app.route('/all')
def all_view():
    return render_template('all.html')


# Преподаватели по цели изучения
@app.route('/goals/<goal>')
def goal_view(goal):
    with open("teacher_db.json", "r", encoding="utf-8") as file:
        profiles_db = json.load(file)
        goal = goal

    return render_template('goal.html', profiles_db=profiles_db, goal=goal)


# Страница репетитора
@app.route('/profiles/<int:id>')
def profile_view(id):
    if id in range(0, 12):
        with open("teacher_db.json", "r", encoding="utf-8") as file:
            data_base = json.load(file)
            name = data_base[id]['name']
            goals = data_base[id]['goals']
            rating = data_base[id]['rating']
            price = data_base[id]['price']
            about = data_base[id]['about']
            free = data_base[id]['free']
            id = id
            avatar = data_base[id]['picture']
    else:
        abort(404)
    return render_template('profile.html',
                           name=name,
                           goals=goals,
                           rating=rating,
                           price=price,
                           about=about,
                           free=free,
                           id=id,
                           avatar=avatar
                           )


# заявки на подбор
@app.route('/request')
def request_view():
    form = RequestForm()
    return render_template('request.html', form=form)


# заявка на подбор отправлена
@app.route('/request_done', methods=['GET', 'POST'])
def request_done_view():
    form = RequestForm()
    if request.method == 'POST':
        client_data = {
            "name": form.name.data,
            "phone": form.phone.data,
            "objective": dict(form.objective.choices).get(form.objective.data),
            "time": dict(form.time_budget.choices).get(form.time_budget.data)
        }
        try:
            # Check if the JSON file exists and is not empty
            if os.path.exists("request.json") and os.path.getsize("request.json") > 0:
                # Load existing data from the JSON file
                with open("request.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
            else:
                # Initialize data as an empty dictionary if the file is empty or doesn't exist
                data = {}
        except json.decoder.JSONDecodeError:
            # Handle JSONDecodeError if the file is empty or not properly formatted
            data = {}

        # Find the next available index
        index = max(map(int, data.keys()), default=0) + 1

        # Append new client data to the dictionary
        data[str(index)] = client_data

        with open("request.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write('\n')

        return render_template('request_done.html',
                               objective=client_data['objective'],
                               time=client_data['time'],
                               name=client_data['name'],
                               phone=client_data['phone'])
    else:
        return render_template('request.html', form=form)


# здесь будет форма бронирования <id учителя>
@app.route('/booking/<int:tutor_id>/<string:day>/<time>', methods=['GET', 'POST'])
def booking_view(tutor_id, day, time):
    form = UserForm()
    form.clientWeekday.data = day
    form.clientTime.data = time
    form.clientTeacher.data = tutor_id
    with open("teacher_db.json", "r", encoding="utf-8") as file:
        data_base = json.load(file)
        teacher_name = data_base[tutor_id]['name']
        booked_day = ''
        for key, value in days.items():
            if key == day:
                booked_day = value
        avatar = data_base[tutor_id]['picture']
    booked_time = time + ":00"
    return render_template('booking.html',
                           form=form,
                           teacher_name=teacher_name,
                           booked_time=booked_time,
                           booked_day=booked_day,
                           avatar=avatar
                           )


# заявка отправлена
@app.route('/booking_done', methods=['POST', 'GET'])
def booking_done_view():
    form = UserForm()
    post_in_day = form.clientWeekday.data
    booked_day = ''
    for key, value in days.items():
        if post_in_day == key:
            booked_day = value
    booked_time = form.clientTime.data + ':00'
    client_name = form.clientName.data
    client_phone = form.clientPhone.data

    booking_data = {
        "booked_time": booked_time,
        "client_name": client_name,
        "client_phone": client_phone
    }

    with open('booking.json', 'a', encoding='utf-8') as file:
        json.dump(booking_data, file, indent=4, ensure_ascii=False)
        file.write('\n')
    flash("Data is recorded")
    return render_template('booking_done.html',
                           booked_day=booked_day,
                           booked_time=booked_time,
                           client_name=client_name,
                           client_phone=client_phone
                           )


if __name__ == "__main__":
    app.run(debug=True)
