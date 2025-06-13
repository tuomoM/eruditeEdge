from flask import Blueprint, render_template
from services.vocab_service import vocab_service

entry_bp = Blueprint("entry", __name__)

@entry_bp.route("/", methods = ["GET","POST"])
def entry():
    no_of_vocabs = vocab_service.get_total_no_of_vocabs()[0][0]

    return render_template("index.html", total_vocabs = no_of_vocabs)
    