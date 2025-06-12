from flask import Blueprint, render_template, redirect, flash, request, session, get_flashed_messages
from services.user_service import user_service
from services.vocab_service import vocab_service

user_bp = Blueprint("user", __name__)

@user_bp.route("/login", methods = ["POST", "GET"])

def login():
    
    username = ""
    error = ""
    if request.method == "POST":
     
        username = request.form["username"]
        password = request.form["password"]
        id = user_service.login(username,password)
        if id:
            session["username"] = username
            session["user_id"] = id
            return redirect("/")
        flash("Incorrect password or username", "error" )
       

    return render_template("login.html", username = username)


@user_bp.route("/user_info", methods = ["POST","GET"])

def user_info():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    vocab_stats = vocab_service.get_users_vocab_stats(user_id)

    total_vocabs = vocab_stats[0]
    total_global = vocab_stats[1]
    training_sessions = vocab_service.get_users_trainings(user_id)
    total_trainings = len(training_sessions)
    return render_template("user.html",trainings = training_sessions, total_trainings = total_trainings, total_vocabs = total_vocabs, total_global = total_global)
    
    
