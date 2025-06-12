from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

vocab_bp = Blueprint("vocab", __name__)

@vocab_bp.route("/maintain", methods = ["POST", "GET"])
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

@vocab_bp.route("/view/<int:id>", methods = ["POST", "GET"])
def view(id:int):
    if "user_id" not in session:
        return redirect("/")
    vocab = vocab_service.get_vocab(id)
    return render_template("view.html", vocab = vocab)    
