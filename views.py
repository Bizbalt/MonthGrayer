from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect
from MonthGreyer import MonthGreyer
import os
views = Blueprint(__name__, "views")


@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'), 'favicon_dark.ico')


#some random dictionary for testing
all_data = {"start_day":"2024-02-18",
            "day_array":[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            "user_access_array":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]}


@views.route("/")
def home():
    return redirect("/MonthGreyer")


@views.route("/process_selected_option", methods=["GET"])
def process_selected_option():
    selected_option = request.args.get("selected")
    # Process the selected option (perform some action, manipulate data, etc.)
    # Example: you can return a JSON response
    return jsonify({'selected_option': selected_option})


@views.route("/MonthGreyer")
def intro_page():
    return render_template("MonthGreyer.html")


@views.route("/grey_day/<string:username>/<string:day>")
def grey_day(username, day):
    calendar_data = MonthGreyer(username)
    success = calendar_data.grey_day(day)
    return str(success)

@views.route("/free_day/<string:username>/<string:day>")
def free_day(username, day):
    calendar_data = MonthGreyer(username)
    success = calendar_data.free_day(day)
    return str(success)

@views.route('/user/<string:username>')
def command(username=None):
    # checking for existing user - might not exist yet
    users = open("users.txt").read().splitlines()

    if not username in users:
        return "no user found"
    
    calendar_data = MonthGreyer(username)
    return jsonify(calendar_data.get_markings())