from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout", methods = ["GET"])
def logout():
    del session["username"],session["user_id"]
    return redirect("/")
