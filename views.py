from flask import Blueprint, render_template, request

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html", value_to_pass="some random value")


@views.route("/about/<page_number>")
def about(page_number):
    return render_template("index.html", value_to_pass="This is number {} of the the about pages.".format(page_number))


@views.route("/personal message")
def personal_message():
    args = request.args  # send query with "/personal message?msg= whatever here"
    msg = args.get("msg")
    msg2 = args.get("msg2")
    return render_template("index.html", value_to_pass=msg, another_value_to_pass=msg2)
