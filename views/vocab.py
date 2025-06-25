from flask import Blueprint, render_template, request,flash, redirect, session,abort
from services.vocab_service import vocab_service

vocab_bp = Blueprint("vocab", __name__)


@vocab_bp.before_request
def before():
    if "user_id" not in session:
        return redirect("/")
    if request.method == "POST":
        if request.form["csrf_token"] != session["csrf_token"]:
           abort(403)

@vocab_bp.route("/create_vocab", methods = ["POST","GET"])
def create_vocab():
    if request.method == "POST":
        word = request.form["word"]
        description = request.form["description"]
        example = request.form["example"]
        synomyms = request.form["synonyms"]
        global_flag = request.form["global_flag"]
        error = vocab_service.add_vocab(word,description,example,synomyms,session["user_id"],global_flag)
        if error:
            flash(error, "error")
        else:
            flash("Vocab created")  
        return redirect("/vocab_list")
    
    visibilities = vocab_service.get_vocab_categories()
    return render_template("create_vocab.html", visibilities = visibilities)

@vocab_bp.route("/vocab_list", methods = ["GET"])
def vocab_list():
    vocabs = vocab_service.get_vocabs(session["user_id"]) 
    return render_template("vocab_list.html", vocabs = vocabs)
@vocab_bp.route("/vocab_list", methods = ["POST"])
def vocab_list_search():
    search_term = request.form["search_term"]
    vocabs = vocab_service.find_by_word(search_term,session["user_id"])
    return render_template("vocab_list.html", vocabs = vocabs)
@vocab_bp.route("/view/<int:id>", methods = ["GET"])
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
            return render_template("confirm_deletion.html", vocab = vocab)
        word = request.form["word"]
        description = request.form["description"]
        example = request.form["example"]
        synonyms = request.form["synonyms"]
        global_flag = request.form["global_flag"]
        error = vocab_service.edit_vocab(vocab ,word, description, example, synonyms, global_flag)
        if error:
            flash(error, "error")
            return render_template("/edit.html", vocab = vocab)
        return redirect("/vocab_list")
    
@vocab_bp.route("/confirm_deletion/<int:vocab_id>", methods = ["POST"])
def confirm_deletion(vocab_id:int):
    vocab = vocab_service.get_vocab(vocab_id)
    if not vocab or vocab["user_id"] != session["user_id"]:
        abort(404)
    result = vocab_service.delete_vocab(vocab_id)
    if result:
        flash(result)
        return redirect("/edit/"+str(vocab_id))
    return redirect("/vocab_list")
    
@vocab_bp.route("/search", methods = ["POST", "GET"])
def search():
    
    if request.method == "POST":        
        search_term = request.form["search_t"]
        vocabs = vocab_service.find_by_word(search_term, session["user_id"])
        if vocabs:
            if "training_id" in session:
                del session["training_id"]
            return render_template("search.html", vocabs = vocabs, search_t = search_term) 
        flash("No entries found")
                 
    return render_template("search.html")

# Suggestion handling
@vocab_bp.route("/suggest_changes/<int:vocab_id>", methods = ["GET","POST"])
def suggest_changes(vocab_id:int):
    vocab = vocab_service.get_vocab(vocab_id)
    if not vocab:
        abort(404)
    if request.method == "GET":
        return render_template("suggest_changes.html", vocab = vocab)
    #POST
    new_description = ""
    new_synonyms = ""
    new_example = ""
    comments = ""
    if "new_description" in request.form:
        new_description = request.form["new_description"]
    if "new_example" in request.form:
        new_example = request.form["new_example"]
    if "new_synonyms" in request.form:
        new_synonyms = request.form["new_synonyms"]
    if "comments" in request.form:
        comments = request.form["comments"]    
 
    result = vocab_service.create_change_suggestion(vocab_id,session["user_id"],new_description,new_example,new_synonyms,comments)
    if result is None:
        flash("Suggestion succesfully saved")
        return redirect("/vocab_list")
    flash("error "+str(result))
    return render_template("suggest_changes.html", vocab = vocab)

        
@vocab_bp.route("/inbox", methods = ["GET", "POST"])
def inbox():
    user_id = session["user_id"]
    suggestions = vocab_service.get_suggestions_to(user_id)
    own_suggestions = vocab_service.get_own_suggestions(user_id)
    return render_template("suggestion_inbox.html", suggestions = suggestions, own_suggestions = own_suggestions )

@vocab_bp.route("/inbox/accept_suggestion/<int:suggestion_id>", methods = ["POST"])
def accept_suggestion(suggestion_id:int):
    error = vocab_service.accept_suggestion(suggestion_id,session["user_id"])
    if error:
        flash(error)
    else:
        flash("Suggestion approved")    
    return redirect("/inbox")    

@vocab_bp.route("/inbox/reject_suggestion/<int:suggestion_id>", methods = ["POST"])
def reject_suggestion(suggestion_id:int):
    error = vocab_service.reject_suggestion(suggestion_id,session["user_id"])
    if error:
        flash(error)
    else:
        flash("Suggestion rejected")    
    return redirect("/inbox") 

@vocab_bp.route("/inbox/cancel_suggestion/<int:suggestion_id>", methods = ["POST"])
def cancel_suggestion(suggestion_id:int):
    error = vocab_service.cancel_suggestion(suggestion_id,session["user_id"])
    if error:
        flash(error)
    else:
        flash("Suggestion cancelled")    
    return redirect("/inbox")       
