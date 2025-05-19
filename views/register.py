from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods = ["POST", "GET"])
def register():
    username = ""
    if request.method == "POST":
        session["_flashes"].clear()
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        return_value = user_service.register(username,password, password2)
        if type(return_value, int):
            session["username"] = username
            session["userid"] = return_value
            return redirect("/")
        flash(return_value, "error" )
       
    
    return render_template("register.html", username = username)

            
