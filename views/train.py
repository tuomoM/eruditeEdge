from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

train_bp = Blueprint("train_fl", __name__)

@train_bp.route("/train_fl/<string:search_term>", methods = ["POST", "GET"])
def train_fl(search_term):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    vocabs = vocab_service.find_by_word(search_term,user_id)
    return render_template("practiceFlash.html", vocabs = vocabs)


@train_bp.route("/init_training", methods = ["GET","POST"])
def init_training():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    vocabs = vocab_service.get_vocabs(user_id)
    return render_template("select.html", vocabs = vocabs)

@train_bp.route("/process_selection", methods = ["POST"]) 
def process_selection():
    return redirect("/")