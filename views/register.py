from flask import Blueprint, render_template, request,flash, redirect
from services.user_service import user_service

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods = ["POST", "GET"])
def register():
    username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        password2 = request.form["password2"]
        error = user_service.register(username,password, password2)
        if not error:
            return redirect("/")
        flash(error,"error")
    
    return render_template("register.html", username = username)

            
