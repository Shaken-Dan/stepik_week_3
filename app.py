import json

from flask import Flask, render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField

app = Flask(__name__)
app.secret_key = "afasfasfaf848a4sf8as41f5a1sf15"


class UserForm(FlaskForm):
    clientName = StringField("Вас зовут")
    clientPhone = IntegerField("Ваш телефон")
    submit = SubmitField("Записаться на пробный урок")
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()


@app.route('/')
def index():
    return render_template('index.html')


# Все репетиторы
@app.route('/all')
def all_view():
    return render_template('all.html')


# Преподаватели по цели изучения
@app.route('/goals/<goal>')
def goal_view(goal):
    return render_template('goal.html')


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
    return render_template('request.html')


# заявка на подбор отправлена
@app.route('/request_done')
def request_done_view():
    return render_template('request_done.html')


# здесь будет форма бронирования <id учителя>
@app.route('/booking/<int:tutor_id>/<string:day>/<time>', methods=['GET', 'POST'])
def booking_view(tutor_id, day, time):
    days = {'mon': 'Понедельник',
            'tue': "Persembe",
            'wed': "Среда",
            'thu': "Четверг",
            'fri': "Жұма",
            'sat': "Сенбі",
            'sun': "Воскресенье"
            }
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
@app.route('/booking_done')
def booking_done_view():
    return render_template('booking_done.html')


if __name__ == "__main__":
    app.run(debug=True)
