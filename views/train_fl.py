from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service

train_fl_bp = Blueprint("train_fl", __name__)

@train_fl_bp.route("/train_fl/<vocabs>", methods = ["POST", "GET"])
def train_fl(vocabs):
    print("train routine reached, with: ")
    print(len(vocabs))
    if not session["user_id"]:
        return redirect("/")
  
    return render_template("practiceFlash.html", vocabs = vocabs)
