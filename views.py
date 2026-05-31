import json
from flask import Blueprint, render_template, jsonify, send_from_directory, redirect
from MonthGrayer import MonthGrayer, get_settings_page, create_new_user, update_user_group, update_group_defaults
import os

from app import limiter

views = Blueprint("views", __name__)


@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static/images'), 'favicon_dark.ico')


@views.route('/robots.txt')
def robots_txt():
    return send_from_directory(os.path.join(views.root_path, 'static'), 'robots.txt')


@views.route("/impressum")
def impressum():
    return render_template("Impressum.html")


@views.route("/")
def home():
    return redirect("/MonthGrayer")


@views.route("/MonthGrayer")
def intro_page():
    return render_template("MonthGrayer.html")


@views.route("/gray_day/<string:username>/<string:day_distance>")
def gray_day(username, day_distance):
    calendar_data = MonthGrayer(username)
    success = calendar_data.gray_day(int(day_distance))
    return str(success)


@views.route("/free_day/<string:username>/<string:day_distance>")
def free_day(username, day_distance):
    calendar_data = MonthGrayer(username)
    success = calendar_data.free_day(int(day_distance))
    return str(success)


@views.route("/de_gray_day/<string:username>/<string:day_distance>")
def de_gray_day(username, day_distance):
    calendar_data = MonthGrayer(username)
    success = calendar_data.de_gray_day(int(day_distance))
    return str(success)


def check_user_exist(username):
    # checking for existing user (the file does not contain the "holiday users")
    users = json.load(open("data/users.json"))
    if username not in users:
        return False
    return True


@views.route('/user/<string:username>')
@limiter.limit("100 per hour")
def serve_userdata(username=None):
    if not (check_user_exist(username)):
        return "no user found"
    calendar_data = MonthGrayer(username)
    return jsonify(calendar_data.get_choice_markings())


@views.route("/settings/<string:username>")  # I can send invites with prior set names with this Link
def settings(username):
    if not (check_user_exist(username)):
        create_new_user(username)
    return render_template("settings.html", username=username)


@views.route("/user_group_settings/<string:username>")
def user_group_settings(username):
    return jsonify(get_settings_page(username))


@views.route("/user_group_update/<string:username>/<string:group>")
def user_group_update(username, group):
    state = update_user_group(username, group)
    return state


@views.route("/user_group_default/<string:defaults>/<string:group>")
def user_group_defaults(defaults, group):
    state = update_group_defaults(defaults, group)
    return state
