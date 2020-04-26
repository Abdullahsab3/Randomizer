import os
import random

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    if "people" not in session:
        session["people"] = []
    if "output" not in session:
        session["output"] = []
    if request.method == "GET":
        return render_template("name_picker.html")
    if request.method == "POST":
        names = request.form.get("names")
        session["people"] = names.split(",")
        session["output"] = random.choice(session["people"])
        return render_template("output")

@app.route("/team-generator", methods=["GET", "POST"])
def team_generator():
    """Team generator"""
    if "people" not in session:
        session["people"] = []
    if "output" not in session:
        session["output"] = []
    if request.method == "GET":
        return render_template("team_generator.html")
    if request.method == "POST":
        names = request.form.get("names")
        session["people"] = names.split(",")
        number_people = len(session["people"])
        number_of_teams = int(request.form.get("number"))
        if number_of_teams <= 0:
            return apology("Must provide a positive number", 400)
        while number_people > 0 and number_of_teams > 0:
            team = random.sample(session["people"], int(number_people/number_of_teams))
            for x in team:
                session["people"].remove(x)
            number_people -= int(number_people/number_of_teams)
            number_of_teams -= 1
            session["output"].append(team)
        return render_template("output.html", output = session["output"])

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
