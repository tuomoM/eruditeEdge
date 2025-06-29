from flask import Blueprint, render_template, request,flash, redirect, session,abort
from services.vocab_service import vocab_service

user_info_bp = Blueprint("user_info", __name__)


@user_info_bp.before_request
def before():
    if "user_id" not in session:
        return redirect("/")
    if request.method == "POST":
        if request.form["csrf_token"] != session["csrf_token"]:
           abort(403)

@user_info_bp.route("/user_info")
def user_info():
    users_stats = vocab_service.get_users_stats(session["user_id"])
    #Add community stats
    return render_template("user.html", user_stats = users_stats)