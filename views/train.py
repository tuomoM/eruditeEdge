from flask import Blueprint, render_template, request,flash, redirect, session
from services.vocab_service import vocab_service
train_bp = Blueprint("train", __name__)
@train_bp.before_request
def before():
    if "user_id" not in session:
        return redirect("/")
    
@train_bp.route("/train_fl/<string:search_term>", methods = ["POST", "GET"])
def train_fl(search_term):
    user_id = session["user_id"]
    vocabs = vocab_service.find_by_word(search_term,user_id)
    return render_template("practiceFlash.html", vocabs = vocabs)


@train_bp.route("/init_training", methods = ["GET","POST"])
def init_training():
    user_id = session["user_id"]
    vocabs = vocab_service.get_vocabs(user_id)
    return render_template("select.html", vocabs = vocabs)

@train_bp.route("/process_selection", methods = ["POST"]) 
def process_selection():
    practice_mode = request.form.get("practice_mode") 
    selected_vocab_ids = request.form.getlist("vocab_ids")
    if len(selected_vocab_ids) < 2:
        flash("Option only available with 2 or more vocabs")
        return redirect("/init_training")
    training_id = vocab_service.get_training_id(session["user_id"],selected_vocab_ids)
    session["training_id"] = training_id

    vocabs = vocab_service.get_vocabset(session["user_id"], selected_vocab_ids)
    if practice_mode == "flashcards":
        return render_template("practiceFlash.html", vocabs = vocabs)
    else:
        return render_template("test.html", vocabs = vocabs)



@train_bp.route("/submit_test", methods = ["POST"])
def submit_test():
    if "training_id" not in session:
        return redirect("/init_training")
    training_id = session["training_id"]
    answers = request.form.get("answers",{})
    form_data = request.form.to_dict()
    for keys in form_data:
        if "answer" in keys:
            answers[keys.split("-")[1]] = form_data[keys]

    results = vocab_service.check_answers(training_id,answers)
    total_queried = len(results)
    total_correct = sum(1 for result in results if result["correctness"])
    vocab_service.update_training(training_id,total_correct/total_queried)
    return render_template('testResults.html', results=results, total_questions=total_queried, total_correct=total_correct)

@train_bp.route("/delete_training/<int:id>", methods = ["POST","GET"])
def delete_training(id:int):
    vocab_service.delete_training(id,session["user_id"])
    return redirect("/user_info")

@train_bp.route("/test_id/<int:id>", methods = ["POST","GET"])
def test_id(id:int):
    session["training_id"] = id
    vocabs = vocab_service.get_training_set(id,session["user_id"])
    if "error" in vocabs: # This needs to be changed, as it makes error a forbidden word in vocabs
        flash(vocabs)
        return redirect("/user_info")
    return render_template("test.html", vocabs = vocabs)

@train_bp.route("/user_info", methods = ["POST","GET"])

def user_info():

    user_id = session["user_id"]
    vocab_stats = vocab_service.get_users_vocab_stats(user_id)

    total_vocabs = vocab_stats[0]
    total_global = vocab_stats[1]
    training_sessions = vocab_service.get_users_trainings(user_id)
    total_trainings = len(training_sessions)
    return render_template("user.html",trainings = training_sessions, total_trainings = total_trainings, total_vocabs = total_vocabs, total_global = total_global)