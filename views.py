from flask import Blueprint, render_template, jsonify, send_from_directory, redirect
from MonthGreyer import MonthGreyer
import os

views = Blueprint(__name__, "views")


@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'), 'favicon_dark.ico')


@views.route("/")
def home():
    return redirect("/MonthGreyer")


@views.route("/MonthGreyer")
def intro_page():
    return render_template("MonthGreyer.html")


@views.route("/grey_day/<string:username>/<string:day_distance>")
def grey_day(username, day_distance):
    calendar_data = MonthGreyer(username)
    success = calendar_data.grey_day(int(day_distance))
    return str(success)


@views.route("/free_day/<string:username>/<string:day_distance>")
def free_day(username, day_distance):
    calendar_data = MonthGreyer(username)
    success = calendar_data.free_day(int(day_distance))
    return str(success)


@views.route("/de_grey_day/<string:username>/<string:day_distance>")
def de_grey_day(username, day_distance):
    calendar_data = MonthGreyer(username)
    success = calendar_data.de_grey_day(int(day_distance))
    return str(success)


@views.route('/user/<string:username>')
def command(username=None):
    # checking for existing user (the file doe not contain the holiday "users")
    users = open("data/users.txt").read().splitlines()

    if username not in users:
        return "no user found"

    calendar_data = MonthGreyer(username)
    return jsonify(calendar_data.get_choice_markings())


@views.route("/settings/<string:username>")
def settings(username):
    return render_template("settings.html", username=username)
