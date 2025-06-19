from flask import Blueprint, render_template, redirect, flash, request, session
from services.user_service import user_service
import secrets

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
            session["csrf_token"] = secrets.token_hex(16)
            flash("login successful")
            return redirect("/")
        flash("Incorrect password or username", "error" )
       

    return render_template("login.html", username = username)



    
    
@user_bp.route("/register", methods = ["POST", "GET"])
def register():
    username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        return_value = user_service.register(username,password, password2)
        if type(return_value)==int:
            session["username"] = username
            session["user_id"] = return_value
            session["csrf_token"] = secrets.token_hex(16)
            flash("userid successfully created")
            return redirect("/")
        flash(return_value, "error" )
       
    
    return render_template("register.html", username = username)

@user_bp.route("/logout", methods = ["GET"])
def logout():
    del session["username"],session["user_id"]
    return redirect("/")
