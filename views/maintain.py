from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service

maintain_bp = Blueprint("maintain", __name__)

@maintain_bp.route("/maintain", methods = ["POST", "GET"])
def maitain():
    if not session["userid"]:
        return redirect("/")
    
       
    
    return render_template("maintain.html")