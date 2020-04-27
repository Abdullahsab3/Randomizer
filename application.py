import os
import random
from cs50 import SQL

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/name-picker", methods=["GET", "POST"])
def name_picker():
    """name picker"""
    # add following dict's to user session if they are not already there.
    if "people" not in session:
        session["people"] = []
    if "output" not in session:
        session["output"] = []
    # return the page if users requests it.
    if request.method == "GET":
        session.clear()
        return render_template("name_picker.html")
    # get information from user.
    if request.method == "POST":
        names = request.form.get("names")
        # split the string to a list
        session["people"] = names.split(",")
        # Get a random element from the list.
        session["output"] = random.choice(session["people"])
        flash("Randomized!")
        return render_template("output.html", output = session["output"])

@app.route("/team-generator", methods=["GET", "POST"])
def team_generator():
    """Team generator"""
    # add following dict's to user session if they are not already there.
    if "people" not in session:
        session["people"] = []
    if "output" not in session:
        session["output"] = []
    # return the page if users requests it.
    if request.method == "GET":
        session.clear()
        return render_template("team_generator.html")
    # get information from the user.
    if request.method == "POST":
        names = request.form.get("names")
        # split the string and store it in a list
        session["people"] = names.split(",")
        number_people = len(session["people"])
        number_of_teams = int(request.form.get("number"))
        # error checking
        if number_of_teams <= 0:
            return apology("You Must provide a positive number", 400)
        # pick random teams.
        while number_people > 0 and number_of_teams > 0:
            teams = random.sample(session["people"], int(number_people/number_of_teams))
            for x in teams:
                session["people"].remove(x)
            number_people -= int(number_people/number_of_teams)
            number_of_teams -= 1
            session["output"].append(teams)
        flash("Randomized!")
        return render_template("output.html", output = session["output"])


@app.route("/name-generator", methods=["GET", "POST"])
def name_generator():
    # read the names database.
    db = SQL("sqlite:///database.db")
    # display the page if user requests it.
    if request.method == "GET":
        return render_template("name_generator.html")
    # get information from user
    if request.method == "POST":
        option = request.form.get("customRadio")
        # get information from database
        if option == "male":
            a = db.execute("SELECT * FROM male WHERE male IN (SELECT male FROM male ORDER BY RANDOM() LIMIT 1)")
            m = a[0]["male"]
        elif option == "female":
            a = db.execute("SELECT * FROM female WHERE female IN (SELECT female FROM female ORDER BY RANDOM() LIMIT 1)")
            m = a[0]["female"]
        else:
            a = db.execute("SELECT * FROM names WHERE names IN (SELECT names FROM names ORDER BY RANDOM() LIMIT 1)")
            m = a[0]["names"].capitalize()
        flash("Randomized!")
        return render_template("output.html", n = m)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
@app.route("/color-generator")
def color_generator():
    # thanks to Dmitry Dubovitsky for his help. https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
    r = lambda: random.randint(0,255)
    code = str('#%02X%02X%02X' % (r(),r(),r()))
    print(code)
    return render_template("color_generator.html", hex = code)

@app.route("/about")
def about():
    return render_template("about.html")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
