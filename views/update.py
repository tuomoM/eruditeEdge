from flask import Blueprint, render_template, request,flash, redirect, session, abort
from services.vocab_service import vocab_service

update_bp = Blueprint("ipdate", __name__)

@update_bp.route("/update/<int:id>", methods = ["POST"])
def update(id:int):
    if not session["user_id"]:
        return redirect("/")
    
 

    
    if request.method == "POST":
        if "user_id" not in session:
            return redirect("/")
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