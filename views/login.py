from flask import Blueprint, render_template, redirect, flash, request, session
from services.user_service import user_service

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods = ["POST", "GET"])
def login():
    username = ""
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        flash(username)

        password = request.form["password"]
        flash(password)
       
        error = user_service.login(username,password)
        if error == "":
            session["username"] = username
            return redirect("/")
        flash(error, "error" )
       
    
    return render_template("login.html", username = username)