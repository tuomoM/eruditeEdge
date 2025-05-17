from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods = ["POST", "GET"])
def register():
    username = ""
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        flash(username)

        password = request.form["password"]
        flash(password)
        password2 = request.form["password2"]
        flash(password2)
        error = user_service.register(username,password, password2)
        if error == "":
            session["username"] = username
            return redirect("/")
        flash(error, "error" )
       
    
    return render_template("register.html", username = username)

            
