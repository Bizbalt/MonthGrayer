from flask import Blueprint, render_template, jsonify, send_from_directory, redirect
from MonthGreyer import MonthGreyer, get_settings_page, create_new_user, update_user_group, update_group_defaults
import os

views = Blueprint(__name__, "views")

# ToDo include communities e.g.
# community = "Lazinth"
# @views.route(community + '/favicon.ico')


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


def check_user_exist(username):
    # checking for existing user (the file does not contain the holiday "users")
    users = open("data/users.txt").read().splitlines()

    if username not in users:
        return False
    return True


@views.route('/user/<string:username>')
def command(username=None):
    if not (check_user_exist(username)):
        return "no user found"
    calendar_data = MonthGreyer(username)
    return jsonify(calendar_data.get_choice_markings())


@views.route("/settings/<string:username>")
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
