from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods = ["POST", "GET"])
def main():
    
       
    
    return render_template("index.html")