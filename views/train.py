from flask import Blueprint, render_template, request,flash, redirect, session, abort
from services.vocab_service import vocab_service
train_bp = Blueprint("train", __name__)
@train_bp.before_request
def before():
    if "user_id" not in session:
        return redirect("/")
    if request.method == "POST":
        if request.form["csrf_token"] != session["csrf_token"]:
           abort(403)

@train_bp.route("/train_fl/<int:training_id>", methods = ["GET"])
def train_fl(training_id):
    user_id = session["user_id"]
    session["training_id"] = training_id
    vocabs = vocab_service.get_training_set(training_id,user_id)
    return render_template("/practiceFlash.html", vocabs = vocabs )

@train_bp.route("/init_training", methods = ["GET","POST"])
def init_training():
    user_id = session["user_id"]
    vocabs = vocab_service.get_vocabs(user_id)
    return render_template("select.html", vocabs = vocabs)

@train_bp.route("/process_selection", methods = ["POST"])
def process_selection():
    practice_mode = request.form.get("practice_mode")
    session_description = request.form.get("session_description")
    print(session_description)
    selected_vocab_ids = request.form.getlist("vocab_ids")
    if len(selected_vocab_ids) < 2:
        flash("Option only available with 2 or more vocabs")
        return redirect("/init_training")
    training_id = vocab_service.get_training_id(session["user_id"],selected_vocab_ids,session_description) 
    session["training_id"] = training_id

    vocabs = vocab_service.get_vocabset(session["user_id"], selected_vocab_ids)
    if practice_mode == "flashcards":
        return render_template("practiceFlash.html", vocabs = vocabs)
    return render_template("test.html", vocabs = vocabs)

@train_bp.route("/train_menu", methods = ["GET"])
def train_menu():
    trainings = vocab_service.get_users_trainings(session["user_id"])
    return render_template("/train_menu.html", trainings = trainings)

   

@train_bp.route("/submit_test", methods = ["POST"])
def submit_test():
    if "training_id" not in session:
        return redirect("/init_training")
    training_id = session["training_id"]
    answers = {}
    form_data = request.form.to_dict()
    for keys in form_data:
        if "answer" in keys:
            answers[keys.split("-")[1]] = form_data[keys]

    results = vocab_service.check_answers(training_id,answers)
    total_queried = len(results)
    total_correct = sum(1 for result in results if result["correctness"])
    vocab_service.update_training(training_id,total_correct/total_queried)
    vocab_service.update_training_vocabs(results,session["user_id"])
    return render_template('testResults.html', results=results, total_questions=total_queried, total_correct=total_correct)

@train_bp.route("/delete_training/<int:id>", methods = ["POST","GET"])
def delete_training(id:int):
    vocab_service.delete_training(id,session["user_id"])
    return redirect("/train_menu")

@train_bp.route("/test_id/<int:id>", methods = ["POST","GET"])
def test_id(id:int):
    session["training_id"] = id
    vocabs = vocab_service.get_training_set(id,session["user_id"])
    if "error" in vocabs: # This needs to be changed, as it makes error a forbidden word in vocabs
        flash(vocabs)
        return redirect("/user_info")
    return render_template("test.html", vocabs = vocabs)

