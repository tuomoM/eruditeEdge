from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

vocab_bp = Blueprint("vocab", __name__)


@vocab_bp.before_request
def before():
    if "user_id" not in session:
        return redirect("/")

@vocab_bp.route("/maintain", methods = ["POST", "GET"])
def maintain():

    
    if request.method == "POST":
        word = request.form["word"]
        description = request.form["description"]
        example = request.form["example"]
        synomyms = request.form["synonyms"]
        global_flag = request.form["global_flag"]
        error = vocab_service.add_vocab(word,description,example,synomyms,session["user_id"],global_flag)
        if error:
            flash(error, "error")
    
    vocabs = vocab_service.get_vocabs(session["user_id"])
    visibilities = vocab_service.get_vocab_categories()
    
    return render_template("maintain.html", vocabs = vocabs, visibilities = visibilities)

@vocab_bp.route("/view/<int:id>", methods = ["POST", "GET"])
def view(id:int):

    vocab = vocab_service.get_vocab(id)
    return render_template("view.html", vocab = vocab)    

@vocab_bp.route("/edit/<int:id>", methods = ["POST", "GET"])
def edit(id:int): 
    vocab = vocab_service.get_vocab(id)
    visibilities = vocab_service.get_vocab_categories()

    if session["user_id"] != vocab["user_id"]:
        return redirect("/maintain")
     
    return render_template("/edit.html", vocab = vocab, visibilities = visibilities)

@vocab_bp.route("/update/<int:id>", methods = ["POST"])
def update(id:int):

    if request.method == "POST":
        vocab = vocab_service.get_vocab(id)
        if session["user_id"] != vocab["user_id"]:
            flash("You cannot edit vocabs created by other users")
            return render_template("/edit.html", vocab = vocab)        
        if "delete" in request.form:
            result = vocab_service.delete_vocab(vocab["id"])
            if result:
                flash(result)
                return render_template("/edit.htlm", vocab = vocab)
            return redirect("/maintain")

        word = request.form["word"]
        description = request.form["description"]
        example = request.form["example"]
        synonyms = request.form["synonyms"]
        global_flag = request.form["global_flag"]
        error = vocab_service.edit_vocab(vocab ,word, description, example, synonyms, global_flag)
        if error:
            flash(error, "error")
            return render_template("/edit.html", vocab = vocab)
        return redirect("/maintain")
    
@vocab_bp.route("/search", methods = ["POST", "GET"])
def search():
    
    if request.method == "POST":        
        search_term = request.form["search_t"]
        vocabs = vocab_service.find_by_word(search_term, session["user_id"])
        if vocabs:
            del session["training_id"]
            return render_template("search.html", vocabs = vocabs, search_t = search_term) 
        else:
            flash("No entries found")
                 
    return render_template("search.html")