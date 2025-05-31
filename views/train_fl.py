from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

train_fl_bp = Blueprint("train_fl", __name__)

@train_fl_bp.route("/train_fl/<string:search_term>", methods = ["POST", "GET"])
def train_fl(search_term):
    if not session["user_id"]:
        return redirect("/")
    user_id = session["user_id"]
    vocabs = vocab_service.find_by_word(search_term,user_id)
    return render_template("practiceFlash.html", vocabs = vocabs)
