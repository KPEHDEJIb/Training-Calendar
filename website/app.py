import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def get_nearest_monday():
    today = datetime.today()
    days_until_monday = today.weekday()

    return today + timedelta(days=days_until_monday)


@app.route("/get_exercises/<string:start_monday>")
def get_exercises(start_monday: str):
    with open("../_trashcan/exercises.json", 'r', encoding="utf-8") as f:
        data = json.load(f)

    start_monday = datetime(*list(map(int, start_monday.split('-'))))
    exercises_with_dates = []

    for week_id, week in enumerate(data["weeks"]):
        for day, exercises in week.items():
            day_id = {"Monday": 0, "Wednesday": 2, "Friday": 4, "Saturday": 5}[day]
            training_date = start_monday + timedelta(weeks=week_id, days=day_id)

            for exercise_name, exercise_data in exercises.items():
                exercises_with_dates.append({
                    "title": f"<a href=\"/dayinfo/?week={week_id}&day={day_id}\">{exercise_name}</a>",
                    "start": training_date.strftime("%Y-%m-%d"),
                    "date": training_date.strftime("%Y-%m-%d"),
                    "html": True
                })

    return jsonify(exercises_with_dates)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dayinfo/")
def dayinfo():
    week = int(request.args.get("week"))
    day = int(request.args.get("day"))

    with open("../_trashcan/exercises.json", 'r', encoding="utf-8") as f:
        data = json.load(f)

    nearest_monday = get_nearest_monday()
    training_date = nearest_monday + timedelta(weeks=week, days=day)
    exercise_info = []

    for week_data in data["weeks"]:
        if week == data["weeks"].index(week_data):
            for day_name, exercises in week_data.items():
                day_offset = {"Monday": 0, "Wednesday": 2, "Friday": 4, "Saturday": 5}
                if day_name in day_offset and day_offset[day_name] == day:
                    for exercise_name, exercise_data in exercises.items():
                        if exercise_data:
                            exercise_info.append(f"{exercise_name}: {exercise_data}")
                        else:
                            exercise_info.append(exercise_name)

    return render_template("exercises.html", date=training_date.strftime("%Y-%m-%d"), exercise_info=exercise_info)


if __name__ == "__main__":
    app.run(debug=True)
