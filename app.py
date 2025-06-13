from flask import Flask, Blueprint, session
from flask import render_template
import db
from views import user, vocab, train, entry
import config



def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key
    app.register_blueprint(user.user_bp)
    app.register_blueprint(vocab.vocab_bp)
    app.register_blueprint(train.train_bp)
    app.register_blueprint(entry.entry_bp)

    return app