from flask import Blueprint, render_template, request,flash, redirect, session
from services.user_service import user_service
from services.vocab_service import vocab_service

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods = ["POST", "GET"])
def main():
    
    if session["user_id"]:
        if request.method == "POST":
            if "train" in request.form:
                print("train button registered")
                return render_template("practiceFlash.html", vocabs = request.form["vocabs"])
            
            print("no train button registerd")
            search_term = request.form["search_t"]
            vocabs = vocab_service.find_by_word(search_term, session["user_id"])
            if vocabs:
                return render_template("index.html", vocabs = vocabs) 
            else:
                flash("No entries found")
                
    
    return render_template("index.html")