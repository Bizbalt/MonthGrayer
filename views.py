from flask import Blueprint, render_template, request, jsonify, send_from_directory
from MonthGreyer import MonthGreyer
import os
views = Blueprint(__name__, "views")

user = "none"


@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'), 'favicon_dark.ico')


#some random dictionary for testing
all_data = {"start_day":"2024-02-18",
            "day_array":[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            "user_access_array":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]}


@views.route("/")
def home():
    return render_template("index.html", value_to_pass="some random value", day_data=all_data)


@views.route("/cal")
def personal_message():
    args = request.args  # send query with "/cal?msg=10"
    msg = "Month chosen " + args.get("msg")
    import calendar
    msg2 = calendar.month(2023, int(args.get("msg")))
    return render_template("index.html", value_to_pass=msg, another_value_to_pass=msg2)


@views.route("/process_selected_option", methods=["GET"])
def process_selected_option():
    selected_option = request.args.get("selected")
    # Process the selected option (perform some action, manipulate data, etc.)
    # Example: you can return a JSON response
    return jsonify({'selected_option': selected_option})


@views.route("/MonthGreyer")
def intro_page():
    return render_template("MonthGreyer.html")


@views.route('/user/<string:username>')
def command(username=None):

    # checking for existing user - might not exist yet
    users = open("users.txt").read().splitlines()

    if username in users:
        month_greyer = MonthGreyer(username)
    else:
        return "no user found"

    # if user exists, load his data
    if request.method == "POST":
        if request.form["current_user"] in users:
            pass
    # else create new user
    calendar_data = MonthGreyer(user)
    print(username)

    return jsonify(calendar_data.get_markings())


@views.route("/button_fade")
def button_fade():
    return render_template("button_fade.html")
