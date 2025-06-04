from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

maintain_bp = Blueprint("maintain", __name__)

@maintain_bp.route("/maintain", methods = ["POST", "GET"])
def maintain():
    if "user_id" not in session:
        return redirect("/")
    
    if request.method == "POST":
        word = request.form["word"]
        description = request.form["description"]
        example = request.form["example"]
        synomyms = request.form["synonyms"]
        error = vocab_service.add_vocab(word,description,example,synomyms,session["user_id"])
        if error:
            flash(error, "error")
    
    vocabs = vocab_service.get_vocabs(session["user_id"])
 
    


    return render_template("maintain.html", vocabs = vocabs)