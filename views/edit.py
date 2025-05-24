from flask import Blueprint, render_template, request,flash, redirect, session, abort
from services.vocab_service import vocab_service

edit_bp = Blueprint("edit", __name__)

@edit_bp.route("/edit/<int:id>", methods = ["POST", "GET"])
def edit(id:int):
   
    if not session["user_id"]:
        return redirect("/")
    
    vocab = vocab_service.get_vocab(id)
    if session["user_id"] != vocab["user_id"]:
        return redirect("/maintain")
     


    return render_template("/edit.html", vocab = vocab)