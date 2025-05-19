from flask import Blueprint, render_template, redirect, flash, request, session
from services.user_service import user_service

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods = ["POST", "GET"])

def login():
    
    username = ""
    error = ""
    if request.method == "POST":
        session["_flashes"].clear()
        username = request.form["username"]
        password = request.form["password"]
        id = user_service.login(username,password)
        if id:
            session["username"] = username
            session["user_id"] = id
            return redirect("/")
        flash("Incorrect password or username", "error" )
       

    return render_template("login.html", username = username)