from flask import Blueprint, render_template, request, jsonify
from MonthGreyer import MonthGreyer
views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html", value_to_pass="some random value")


@views.route("/about/<page_number>")
def about(page_number):
    return render_template("index.html", value_to_pass="This is number {} of the the about pages.".format(page_number))


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


# aJaX request from input into the "current_user" field
# @views.get("/update")
def update(user):
    print("function called")
    # checking for existing user - might not exist yet
    with open("users.txt", "r") as f:
        users = f.readlines()
    # if user exists, load his data
    if request.method == "POST":
        if request.form["current_user"] in users:
            pass
    # else create new user
    calendar_data = MonthGreyer(user)


@views.route('/<FUNCTION>')
def command(FUNCTION=None):
    exec(FUNCTION.replace("<br>", "\n"))
    print("executed function")
    return ""